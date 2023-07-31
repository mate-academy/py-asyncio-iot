import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
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
    devices = [hue_light, speaker, toilet]

    device_ids = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )

    await run_sequence(
            run_parallel(
                service.send_msg(Message(device_ids[0], MessageType.SWITCH_ON, "")),
                service.send_msg(Message(device_ids[1], MessageType.SWITCH_ON, "")),
                service.send_msg(Message(device_ids[1], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
                ),
            run_parallel(
                service.send_msg(Message(device_ids[0], MessageType.SWITCH_OFF)),
                service.send_msg(Message(device_ids[1], MessageType.SWITCH_OFF)),
                service.send_msg(Message(device_ids[2], MessageType.FLUSH)),
                service.send_msg(Message(device_ids[2], MessageType.CLEAN)),
            )
        )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
