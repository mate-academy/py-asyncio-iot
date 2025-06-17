import time
import asyncio
from typing import Any, Awaitable

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
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    
    results = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )


    # create a few programs
    wake_up_program = [
        Message(results[0], MessageType.SWITCH_ON),
        Message(results[1], MessageType.SWITCH_ON),
        Message(results[1], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(results[0], MessageType.SWITCH_OFF),
        Message(results[1], MessageType.SWITCH_OFF),
        Message(results[2], MessageType.FLUSH),
        Message(results[2], MessageType.CLEAN),
    ]
    
    await run_sequence(service.run_program(wake_up_program[0]), 
                       service.run_program(wake_up_program[1]),
                       service.run_program(wake_up_program[2]))
    await run_parallel(service.run_program(sleep_program[0]),
                       service.run_program(sleep_program[1]),
                       service.run_program(sleep_program[2]),
                       service.run_program(sleep_program[3]))

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
