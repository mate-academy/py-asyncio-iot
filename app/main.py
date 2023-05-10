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

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    device_ids = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    await run_sequence(
        run_parallel(
            service.send_msg(Message(device_ids[0], MessageType.SWITCH_ON)),
            service.send_msg(Message(device_ids[1], MessageType.SWITCH_ON)),
        ),
        service.send_msg(Message(device_ids[1], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")),
        run_parallel(
            service.send_msg(Message(device_ids[0], MessageType.SWITCH_OFF)),
            service.send_msg(Message(device_ids[1], MessageType.SWITCH_OFF)),
            service.send_msg(Message(device_ids[2], MessageType.FLUSH)),
        ),
        service.send_msg(Message(device_ids[2], MessageType.CLEAN))
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
