import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices

    register_devices = [
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    ]
    devices = await asyncio.gather(*register_devices)
    hue_light_id, speaker_id, toilet_id = devices

    wake_up_program = [
        [
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON),
        ],
        [
            Message(speaker_id, MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                    ),
        ]
    ]
    sleep_program = [
        [
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
            Message(toilet_id, MessageType.FLUSH),
        ],
        [
            Message(toilet_id, MessageType.CLEAN),
        ]
    ]
    await service.run_program(wake_up_program[0], wake_up_program[1])
    await service.run_program(sleep_program[0], sleep_program[1])


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
