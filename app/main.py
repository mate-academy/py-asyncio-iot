import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*funcs) -> None:
    for function in funcs:
        await function


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    registered = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )
    hue_light_id, speaker_id, toilet_id = registered

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]

    action_program = [
        Message(
            speaker_id, MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
        Message(toilet_id, MessageType.FLUSH),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await run_sequence(
        service.run_parallel(wake_up_program),
        service.run_parallel(action_program),
        service.run_parallel(sleep_program)
    )

    await asyncio.gather(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
