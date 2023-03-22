import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    speaker_wake_up_program = [
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    hue_light_sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
    ]

    speaker_sleep_program = [
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]

    hue_light_wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
    ]

    toilet_sleep_program = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    print("WAKE UP PROGRAM")
    await run_parallel(
        run_sequence(
            speaker.connect(),
            service.device_operation(speaker_wake_up_program),
        ),
        run_sequence(
            hue_light.connect(),
            service.device_operation(hue_light_wake_up_program),
        ),
        toilet.connect()
    )
    print(f"{'-'* 10}")
    print("SLEEP PROGRAM")
    await run_parallel(
        service.device_operation(toilet_sleep_program),
        service.device_operation(speaker_sleep_program),
        service.device_operation(hue_light_sleep_program)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
