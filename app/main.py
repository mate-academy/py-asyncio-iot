import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable

service = IOTService()


async def run_sequence(*messages: Awaitable[Any]) -> None:
    for message in messages:
        await service.send_msg(message)


async def run_parallel(*messages: Awaitable[Any]) -> None:
    await asyncio.gather(*(service.send_msg(message) for message in messages))


async def main() -> None:
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    await run_parallel(
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON)
    ),
    await run_sequence(
        Message(
            speaker_id, MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    )

    await run_sequence(
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(hue_light_id, MessageType.SWITCH_OFF),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
