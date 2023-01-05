import time
import asyncio

from iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice
)
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Awaitable, Any


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]):
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()
    devices = {
        "hue_light": HueLightDevice(),
        "speaker": SmartSpeakerDevice(),
        "toilet": SmartToiletDevice(),
    }
    devices_coroutines = [
        service.register_device(devices[device])
        for device in devices
    ]

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(*devices_coroutines)

    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    await service.run_program(wake_up_program)
    await service.run_program(sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
