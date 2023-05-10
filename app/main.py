import asyncio
import time
from typing import Awaitable, Any

from iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice
)
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
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    ids = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    hue_light_id, speaker_id, toilet_id = ids

    switch_on = Message(hue_light_id, MessageType.SWITCH_ON)
    speaker_switch_on = Message(speaker_id, MessageType.SWITCH_ON)
    play_song = Message(
        speaker_id,
        MessageType.PLAY_SONG,
        "Rick Astley - Never Gonna Give You Up"
    )

    await run_parallel(service.send_msg
                       (switch_on),
                       service.send_msg(speaker_switch_on)
                       )
    await run_sequence(service.send_msg(play_song))
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(toilet_id, MessageType.FLUSH))

    )
    await run_sequence(service.send_msg(Message(
        toilet_id, MessageType.CLEAN))
    )
    await run_parallel(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id)
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
