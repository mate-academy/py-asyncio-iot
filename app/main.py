import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def print_running_program() -> None:
    print("=====RUNNING PROGRAM======")


async def print_ending_program() -> None:
    print("=====END OF PROGRAM======")


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    devices_id = await asyncio.gather(*[
        service.register_device(device)
        for device in [hue_light, speaker, toilet]
    ])

    await run_sequence(
        print_running_program(),
        run_parallel(
            service.send_msg(
                Message(devices_id[0], MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(devices_id[1], MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(
                    devices_id[1],
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ),
        ),
        print_ending_program()
    )
    await run_sequence(
        print_running_program(),
        run_parallel(
            service.send_msg(
                Message(devices_id[0], MessageType.SWITCH_OFF)
            ),
            service.send_msg(
                Message(devices_id[1], MessageType.SWITCH_OFF)
            ),
            service.send_msg(
                Message(devices_id[-1], MessageType.FLUSH)
            ),
            service.send_msg(
                Message(devices_id[-1], MessageType.CLEAN)
            ),
        ),
        print_ending_program()
    )

    await run_sequence()


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
