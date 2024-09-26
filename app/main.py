import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType


async def main() -> None:

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    devices = [hue_light, speaker, toilet]

    await asyncio.gather(*[device.connect() for device in devices])

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    print("=====RUNNING PROGRAM======")
    await asyncio.gather(
        *[run_parallel(device.send_message(MessageType.SWITCH_ON)) for device in (hue_light, speaker)]
    )
    await asyncio.gather(
        run_sequence(speaker.send_message(MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
    )
    print("=====END OF PROGRAM======")
    print("=====RUNNING PROGRAM======")
    await asyncio.gather(
        *[run_parallel(device.send_message(MessageType.SWITCH_OFF)) for device in (hue_light, speaker)]
    )
    await asyncio.gather(
        *[run_sequence(toilet.send_message(MessageType.FLUSH), toilet.send_message(MessageType.CLEAN))]
    )
    print("=====END OF PROGRAM======")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
