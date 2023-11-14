import time
import asyncio
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
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

    devices_to_register = [
        HueLightDevice(),
        SmartSpeakerDevice(),
        SmartToiletDevice()
    ]
    device_ids = await service.register_device(devices_to_register)

    # create a few programs
    async def wake_up_program() -> None:
        await run_parallel(
            service.send_msg(Message(device_ids[0], MessageType.SWITCH_ON)),
            service.send_msg(Message(device_ids[1], MessageType.SWITCH_ON)),
            service.send_msg(
                Message(device_ids[1],
                        MessageType.PLAY_SONG,
                        "Rick Astley - Never Gonna Give You Up")
            ),
        )

    async def sleep_program() -> None:
        await run_parallel(
            service.send_msg(Message(device_ids[0], MessageType.SWITCH_OFF)),
            service.send_msg(Message(device_ids[1], MessageType.SWITCH_OFF)),
            run_sequence(
                service.send_msg(Message(device_ids[2], MessageType.FLUSH)),
                service.send_msg(Message(device_ids[2], MessageType.CLEAN)),
            ),
        )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
