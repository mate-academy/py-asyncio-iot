import time
import asyncio

from typing import Any, Awaitable
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    hue_light_id = await service.register_device(hue_light)
    speaker_id = await service.register_device(speaker)
    toilet_id = await service.register_device(toilet)

    await run_parallel(
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON, "on")),
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON, "on")),
        service.send_msg(Message(toilet_id, MessageType.FLUSH, "flush"))
    )
    await run_sequence(
        service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "play")),
        service.send_msg(Message(toilet_id, MessageType.CLEAN, "clean"))
    )
    await run_parallel(
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF, "off")),
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF, "off")),
        service.send_msg(Message(toilet_id, MessageType.CLOSE, "close"))
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
