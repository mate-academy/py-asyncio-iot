import asyncio
import time
from typing import Awaitable, Any

from app.iot.service import IOTService
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # run the programs
    await run_sequence(
        # wake up program
        service.run_program([
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up")]),
        # sleep program
        service.run_program([
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
            Message(toilet_id, MessageType.FLUSH),
            Message(toilet_id, MessageType.CLEAN)])
    )
    await asyncio.gather(
        hue_light.disconnect(),
        speaker.disconnect(),
        toilet.disconnect(),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
