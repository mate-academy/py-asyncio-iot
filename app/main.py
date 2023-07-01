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
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    registers = await asyncio.gather(
        *[service.register_device(device)
          for device in (hue_light, speaker, toilet)]
    )
    hue_light_id = registers[0]
    speaker_id = registers[1]
    toilet_id = registers[2]

    # create a few programs
    parallel_program_wake_up = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]

    parallel_program_action = [
        Message(toilet_id, MessageType.FLUSH),
        Message(
            speaker_id,
            MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    parallel_program_sleep = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await run_sequence(
        run_parallel(
            *[service.run_program([program])
              for program in parallel_program_wake_up]
        ),
        run_parallel(
            *[service.run_program([program])
              for program in parallel_program_action]
        ),
        run_parallel(
            *[service.run_program([program])
              for program in parallel_program_sleep]
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
