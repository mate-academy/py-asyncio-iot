import asyncio
import logging
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    )

    # Wake Up Program
    logging.info("Devices registered successfully!")

    logging.info("Waking Up Devices...")
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
    )
    await service.send_msg(
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        )
    )
    logging.info("Devices are awake!")

    logging.info("Putting Devices to Sleep...")
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
    )
    await run_sequence(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )
    logging.info("Devices are asleep!")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    logging.info(f"Elapsed: {end - start: .2f} seconds")
