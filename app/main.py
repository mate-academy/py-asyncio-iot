import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*coros):
    """
    Await coroutines sequentially (one after the other),
    preserving logical ordering.
    """
    for coro in coros:
        await coro


async def run_parallel(*coros):
    """
    Run coroutines concurrently.
    """
    await asyncio.gather(*coros)


async def main() -> None:
    service = IOTService()

    # create device instances
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # register/connect devices concurrently (requires service.register_devices as async)
    # if your service only has register_device (async version), call it per-device with await.
    device_ids = await service.register_devices([hue_light, speaker, toilet])
    hue_light_id, speaker_id, toilet_id = device_ids

    # Compose the wake-up flow:
    # - Hue SWITCH_ON can run in parallel with the speaker sequence
    # - Speaker must SWITCH_ON before PLAY_SONG, so we use run_sequence for those two
    wake_flow = run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(
                Message(
                    speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
                )
            ),
        ),
    )

    # Compose the sleep flow:
    # - Hue SWITCH_OFF and Speaker SWITCH_OFF can run in parallel with the toilet sequence
    # - Toilet FLUSH must precede CLEAN, so we use run_sequence for those two
    sleep_flow = run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        ),
    )

    # Run both composed flows concurrently while preserving each flow's internal order
    await asyncio.gather(wake_flow, sleep_flow)

    # graceful shutdown: disconnect/unregister all (assumes service.unregister_all exists)
    await service.unregister_all()


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
