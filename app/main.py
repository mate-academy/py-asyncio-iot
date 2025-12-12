import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)

async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    tasks = [
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    ]

    result = await asyncio.gather(*tasks)

    await service.run_program(
        [Message(result[0], MessageType.SWITCH_ON),],
        run_parallel
    )
    await service.run_program(
        [Message(result[1], MessageType.SWITCH_ON),
        Message(result[1], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),],
        run_sequence
    )
    await service.run_program(
        [Message(result[0], MessageType.SWITCH_OFF),
        Message(result[1], MessageType.SWITCH_OFF),],
        run_parallel
    )
    await service.run_program(
        [Message(result[2], MessageType.FLUSH),
        Message(result[2], MessageType.CLEAN),],
        run_sequence
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
