import asyncio
import time
from asyncio import TaskGroup

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

from typing import Any, Awaitable

async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    result1 = asyncio.create_task(service.register_device(hue_light))
    result2 = asyncio.create_task(service.register_device(speaker))
    result3 = asyncio.create_task(service.register_device(toilet))
    results = await asyncio.gather(result1, result2, result3)

    hue_light_id, speaker_id, toilet_id = results[0], results[1], results[2]

    hue_light = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(hue_light_id, MessageType.SWITCH_OFF),
    ]
    speaker = [
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]

    toilet = [
        Message(toilet_id, MessageType.FLUSH),
        Message(speaker_id, MessageType.CLEAN),
    ]


    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    # run the programs
    await run_parallel(service.run_program(hue_light),
                       service.run_program(speaker),
                       service.run_program(toilet))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
