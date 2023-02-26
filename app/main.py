import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
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
    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)
    await asyncio.gather(*[hue_light_id, speaker_id, toilet_id])

    # create a few programs
    parallel_start = [
        hue_light.send_message(MessageType.SWITCH_ON),
        speaker.send_message(MessageType.SWITCH_ON),
    ]

    sequence = [
        toilet.send_message(MessageType.FLUSH),
        toilet.send_message(MessageType.CLEAN),
    ]

    parallel_stop = [
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF),
    ]

    # run the programs
    wake_up = [
        print("=====RUNNING PROGRAM======"),
        await run_parallel(*parallel_start),
        await speaker.send_message(
            MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
        print("=====END OF PROGRAM======"),
    ]

    sleep = [
        print("=====RUNNING PROGRAM======"),
        await run_parallel(*parallel_stop),
        await run_sequence(*sequence),
        print("=====END OF PROGRAM======"),
    ]


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
