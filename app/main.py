import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    (hue_light_id, speaker_id, toilet_id) = await asyncio.gather(
        asyncio.to_thread(service.register_device, hue_light),
        asyncio.to_thread(service.register_device, speaker),
        asyncio.to_thread(service.register_device, toilet),
    )
    await run_parallel(
        service.wrap_send_msg_to_thread(
            Message(hue_light_id, MessageType.SWITCH_ON)
        ),
        run_sequence(
            service.wrap_send_msg_to_thread(
                Message(speaker_id, MessageType.SWITCH_ON)
            ),
            service.wrap_send_msg_to_thread(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up",
                )
            ),
        ),
    )

    await run_parallel(
        service.wrap_send_msg_to_thread(
            Message(hue_light_id, MessageType.SWITCH_OFF)
        ),
        service.wrap_send_msg_to_thread(
            Message(speaker_id, MessageType.SWITCH_OFF)
        ),
        run_sequence(
            service.wrap_send_msg_to_thread(
                Message(toilet_id, MessageType.FLUSH)
            ),
            service.wrap_send_msg_to_thread(
                Message(toilet_id, MessageType.CLEAN)
            ),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
