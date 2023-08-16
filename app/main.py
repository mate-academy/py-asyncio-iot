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

    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    task_hue_light_id = await asyncio.create_task(hue_light_id)
    task_speaker_id = await asyncio.create_task(speaker_id)
    task_toilet_id = await asyncio.create_task(toilet_id)

    light_on = service.run_program(
        [Message(task_hue_light_id, MessageType.SWITCH_ON)]
    )
    speaker_on = service.run_program(
        [Message(task_speaker_id, MessageType.SWITCH_ON)]
    )
    speaker_play = service.run_program(
        [
            Message(
                task_speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            )
        ]
    )
    light_off = service.run_program(
        [Message(task_hue_light_id, MessageType.SWITCH_OFF)]
    )
    speaker_off = service.run_program(
        [Message(task_speaker_id, MessageType.SWITCH_OFF)]
    )
    flush = service.run_program([Message(task_toilet_id, MessageType.FLUSH)])
    clean = service.run_program([Message(task_toilet_id, MessageType.CLEAN)])

    await run_parallel(
        light_on,
        speaker_on,
        speaker_play
    )
    await run_parallel(
        light_off,
        speaker_off,
        flush,
        clean
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
