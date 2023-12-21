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

    await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # create a few programs
    song = "Rick Astley - Never Gonna Give You Up"

    light_on = hue_light.send_message(MessageType.SWITCH_ON)
    light_off = hue_light.send_message(MessageType.SWITCH_OFF)

    speaker_on = speaker.send_message(MessageType.SWITCH_ON)
    speaker_off = speaker.send_message(MessageType.SWITCH_OFF)
    speaker_play = speaker.send_message(MessageType.PLAY_SONG, song)

    toilet_flush = toilet.send_message(MessageType.FLUSH)
    toilet_clean = toilet.send_message(MessageType.CLEAN)

    light_and_speaker_on = run_parallel(light_on, speaker_on)
    toilet_use = run_sequence(toilet_flush, toilet_clean)

    morning = run_sequence(light_and_speaker_on, speaker_play)
    evening = run_parallel(light_off, speaker_off, toilet_use)

    await morning

    await evening


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
