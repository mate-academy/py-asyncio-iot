from typing import Any, Awaitable
import asyncio
import time

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
    devices = [hue_light, speaker, toilet]

    devices_ids = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )
    hue_light_id, speaker_id, toilet_id = devices_ids

    # create a few programs
    hue_light_program = Message(hue_light_id, MessageType.SWITCH_ON)
    speaker_program = [
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up",
        ),
    ]
    wake_up_program = run_parallel(
        *[
            service.send_msg(hue_light_program),
            run_sequence(
                *[service.send_msg(command) for command in speaker_program]
            ),
        ]
    )

    shutdown_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]
    toilet_program = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]
    sleep_program = run_parallel(
        *[
            run_parallel(
                *[service.send_msg(command) for command in shutdown_program]
            ),
            run_sequence(
                *[service.send_msg(command) for command in toilet_program]
            ),
        ]
    )

    # run the programs
    await service.run_program(wake_up_program)
    await service.run_program(sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
