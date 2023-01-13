import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    print("=====RUNNING PROGRAM======")
    for function in functions:
        await function
    print("=====END OF PROGRAM======")


async def run_parallel(*functions: Awaitable[Any]) -> None:
    print("=====RUNNING PROGRAM======")
    await asyncio.gather(*functions)
    print("=====END OF PROGRAM======")


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
    await asyncio.gather(*[hue_light_id, speaker_id, toilet_id])

    parallel_on = [
        hue_light.send_message(MessageType.SWITCH_ON),
        speaker.send_message(MessageType.SWITCH_ON),
    ]

    sequence_commands = [
        speaker.send_message(MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        toilet.send_message(MessageType.FLUSH),
        toilet.send_message(MessageType.CLEAN),
    ]

    parallel_off = [
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF),
    ]

    await run_parallel(*parallel_on)

    await run_sequence(*sequence_commands)

    await run_parallel(*parallel_off)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
