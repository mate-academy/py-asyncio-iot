import time
import asyncio
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

    await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # create a few programs
    await run_sequence(
        run_parallel(
            hue_light.send_message(MessageType.SWITCH_ON),
            speaker.send_message(MessageType.SWITCH_ON),
        ),
        speaker.send_message(
            MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
    )

    await run_sequence(
        run_parallel(
            hue_light.send_message(MessageType.SWITCH_OFF),
            speaker.send_message(MessageType.SWITCH_OFF),
        ),
        toilet.send_message(MessageType.FLUSH),
        toilet.send_message(MessageType.CLEAN),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
