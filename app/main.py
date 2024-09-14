import asyncio
import time

from typing import Any, Awaitable, List

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_parallel(*functions: Awaitable[Any]) -> tuple[Any]:
    return await asyncio.gather(*functions)


async def run_program(service: IOTService, messages: List[Message]) -> None:
    await asyncio.to_thread(service.run_program, messages)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    device_ids = await run_parallel(
        asyncio.to_thread(service.register_device, hue_light),
        asyncio.to_thread(service.register_device, speaker),
        asyncio.to_thread(service.register_device, toilet),
    )

    hue_light_id = device_ids[0]
    speaker_id = device_ids[1]
    toilet_id = device_ids[2]

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    wake_task = asyncio.create_task(run_program(service, wake_up_program))
    sleep_task = asyncio.create_task(run_program(service, sleep_program))

    await asyncio.gather(wake_task, sleep_task)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
