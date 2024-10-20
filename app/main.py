import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    devices = [hue_light, speaker, toilet]
    registered_devices = [
        asyncio.create_task(service.register_device(device))
        for device in devices
    ]

    gathered_devices = asyncio.gather(*registered_devices)
    hue_light_id, speaker_id, toilet_id = await gathered_devices

    wake_up_parallel = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]
    wake_up_sequence = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sleep_parallel = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
    ]
    sleep_sequence = [
        Message(toilet_id, MessageType.CLEAN),
    ]

    # wake-up tasks
    await run_parallel(
        asyncio.create_task(
            service.run_program(wake_up_parallel)
        )
    )
    await run_sequence(
        asyncio.create_task(
            service.run_program(wake_up_sequence)
        )
    )

    # sleep tasks
    await run_parallel(
        asyncio.create_task(
            service.run_program(sleep_parallel)
        )
    )
    await run_sequence(
        asyncio.create_task(
            service.run_program(sleep_sequence)
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
