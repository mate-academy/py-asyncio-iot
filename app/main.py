import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*tasks: Awaitable[Any]) -> None:
    """Run tasks one after another (sequentially)."""
    for task in tasks:
        await task


async def run_parallel(*tasks: Awaitable[Any]) -> None:
    """Run tasks concurrently (in parallel)."""
    await asyncio.gather(*tasks)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # Initialize devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # Register devices concurrently
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    print("===== RUNNING WAKE UP PROGRAM =====")
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ),
        ),
    )
    print("===== END OF WAKE UP PROGRAM =====\n")

    print("===== RUNNING SLEEP PROGRAM =====")
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        ),
    )
    print("===== END OF SLEEP PROGRAM =====")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Elapsed: {end - start:.4f} sec.")
