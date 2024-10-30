import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Run tasks in a strict sequence."""
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    """Run tasks in parallel."""
    await asyncio.gather(*functions)


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
        service.register_device(toilet)
    )

    # run wake-up program: turn on light and speaker in parallel, then play the song
    await run_parallel(
            service.send_message(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_message(Message(speaker_id, MessageType.SWITCH_ON))
        )

    # Play song after both light and speaker are on
    await run_sequence(
        service.send_message(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        )
    )

    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_message(Message(speaker_id, MessageType.SWITCH_OFF))
    )

    await run_sequence(
        service.send_message(Message(toilet_id, MessageType.FLUSH)),
        service.send_message(Message(toilet_id, MessageType.CLEAN))
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
