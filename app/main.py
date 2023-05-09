import asyncio
import time
from typing import Any, Awaitable

from app.iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice
)
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()
    song_name = "Rick Astley - Never Gonna Give You Up"

    hue_light = await service.register_device(HueLightDevice())
    speaker = await service.register_device(SmartSpeakerDevice())
    toilet = await service.register_device(SmartToiletDevice())

    wake_up_program = [
        Message(hue_light, MessageType.SWITCH_ON),
        Message(speaker, MessageType.SWITCH_ON),
        Message(toilet, MessageType.PLAY_SONG, song_name),
    ]
    sleep_program = [
        Message(hue_light, MessageType.SWITCH_OFF),
        Message(speaker, MessageType.SWITCH_OFF),
        Message(toilet, MessageType.FLUSH),
        Message(toilet, MessageType.CLEAN),
    ]

    await run_sequence(service.run_program(wake_up_program))
    await run_parallel(service.run_program(sleep_program))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
