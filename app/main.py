import asyncio
import time

from app.iot import service
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice, TIME_TO_SLEEP
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # gather registering devices simultaneously
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # combine run_sequence and run_parallel for wake_up_program
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(
                Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
            ),
        ),
    )

    # combine run_sequence and run_parallel for sleep_program
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
    )

    print("=====END OF PROGRAM======")

    await run_sequence(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


async def run_sequence(*functions: asyncio.Task) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: asyncio.Task) -> None:
    await asyncio.gather(*functions)


if __name__ == "__main__":
    start = time.perf_counter()
    print("=====RUNNING PROGRAM======")
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
