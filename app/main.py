import time
import asyncio
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def register_devices(service: IOTService) -> tuple[int, int, int]:
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    return await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def main() -> None:
    service = IOTService()
    hue_light_id, speaker_id, toilet_id = await register_devices(service)

    await run_sequence(
        asyncio.gather(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            run_sequence(
                service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
                service.send_msg(Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )),
            ),
        ),
        asyncio.gather(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            run_sequence(
                service.send_msg(Message(toilet_id, MessageType.FLUSH)),
                service.send_msg(Message(toilet_id, MessageType.CLEAN)),
            ),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
