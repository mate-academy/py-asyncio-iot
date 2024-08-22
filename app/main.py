import asyncio
import time
from typing import (
    Awaitable,
    Any
)

from iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice
)
from iot.message import (
    Message,
    MessageType
)
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

    # register devices concurrently
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # create a few programs
    wake_up_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        service.send_msg(
            Message(
                speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        ),
    ]

    sleep_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    ]

    # run the programs
    await run_parallel(*wake_up_program)
    await run_parallel(*sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
