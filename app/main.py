import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await parallel_handling(
        asyncio.create_task(service.register_device(hue_light)),
        asyncio.create_task(service.register_device(speaker)),
        asyncio.create_task(service.register_device(toilet))
    )

    # run the programs
    await sequence_handling(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_ON),
                Message(speaker_id, MessageType.SWITCH_ON)
            ]
        ),
        service.run_program(
            [
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ]
        ),
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_OFF),
                Message(speaker_id, MessageType.SWITCH_OFF),
                Message(toilet_id, MessageType.FLUSH)
            ]
        ),
        service.run_program(
            [
                Message(toilet_id, MessageType.CLEAN),
            ]
        ),
    )


async def parallel_handling(*services: Awaitable[Any]) -> tuple:
    return await asyncio.gather(*services)


async def sequence_handling(*services: Awaitable[Any]) -> None:
    for service in services:
        await service


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
