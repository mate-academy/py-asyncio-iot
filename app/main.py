import asyncio
import time
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
    devices_id = await asyncio.gather(
        *[service.register_device(device) for device in (
            HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()
        )]
    )

    hue_light_id, speaker_id, toilet_id = devices_id

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
    # wake up program
    await run_sequence(
        run_parallel(
            *[service.send_msg(msg) for msg in wake_up_program[:-1]]
        ),
        service.send_msg(wake_up_program[-1])
    )
    # sleep program
    await run_sequence(
        run_parallel(
            *[service.send_msg(msg) for msg in sleep_program[:-1]]
        ),
        service.send_msg(sleep_program[-1])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
