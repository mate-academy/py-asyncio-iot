import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
import asyncio

from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # run_parallel
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
``` hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )
    await run_parallel(hue_light_id, speaker_id, toilet_id)
    # create a few programs
    wake_up_program = [
        Message(hue_light_id.result(), MessageType.SWITCH_ON),
        Message(speaker_id.result(), MessageType.SWITCH_ON),
        Message(
            speaker_id.result(),
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sleep_program = [
        Message(hue_light_id.result(), MessageType.SWITCH_OFF),
        Message(speaker_id.result(), MessageType.SWITCH_OFF),
        Message(toilet_id.result(), MessageType.FLUSH),
        Message(toilet_id.result(), MessageType.CLEAN),
    ]

    # run_sequence
    await run_sequence(
        service.run_program(wake_up_program),
        service.run_program(sleep_program)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
