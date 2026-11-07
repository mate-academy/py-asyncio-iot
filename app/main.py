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

    task_hue_light = asyncio.create_task(service.register_device(hue_light))
    task_speaker = asyncio.create_task(service.register_device(speaker))
    task_toilet = asyncio.create_task(service.register_device(toilet))

    hue_light_id = await task_hue_light
    speaker_id = await task_speaker
    toilet_id = await task_toilet

    await run_sequence(
        run_parallel(
            service.run_program(
                [
                    Message(hue_light_id, MessageType.SWITCH_ON),
                    Message(speaker_id, MessageType.SWITCH_ON),
                ]
            )
        ),

        service.run_program(
            [
                Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
            ]
        )
    )

    await run_sequence(
        run_parallel(
            service.run_program(
                [
                    Message(hue_light_id, MessageType.SWITCH_OFF),
                    Message(speaker_id, MessageType.SWITCH_OFF),
                    Message(toilet_id, MessageType.FLUSH),
                ]
            )
        ),
        service.run_program(
            [
                Message(toilet_id, MessageType.CLEAN)
            ]
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
