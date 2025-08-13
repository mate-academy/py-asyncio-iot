import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


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
    hue_light_task = asyncio.create_task(service.register_device(hue_light))
    speaker_task = asyncio.create_task(service.register_device(speaker))
    toilet_task = asyncio.create_task(service.register_device(toilet))
    hue_light_id = await hue_light_task
    speaker_id = await speaker_task
    toilet_id = await toilet_task

    # # create a few programs
    await run_sequence(
        service.run_parallel([
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON),

        ]),
        service.run_parallel([
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        ]),
        service.run_parallel([
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
            Message(toilet_id, MessageType.FLUSH),

        ]),
        service.run_parallel([
            Message(toilet_id, MessageType.CLEAN),
        ])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
