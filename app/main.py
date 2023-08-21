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


async def running_program() -> None:
    print("=====RUNNING PROGRAM======")


async def ending_program() -> None:
    print("=====END OF PROGRAM======")


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    devices = await asyncio.gather(
        *[
            service.register_device(device)
            for device in [hue_light, speaker, toilet]
        ]
    )
    hue_light_id = devices[0]
    speaker_id = devices[1]
    toilet_id = devices[2]

    await run_sequence(
        running_program(),
        run_parallel(
            service.send_msg(
                Message(hue_light_id, MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ),
        ),
        ending_program()
    )
    await run_sequence(
        running_program(),
        run_parallel(
            service.send_msg(
                Message(hue_light_id, MessageType.SWITCH_OFF)
            ),
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_OFF)
            ),
            service.send_msg(
                Message(toilet_id, MessageType.FLUSH)
            ),
            service.send_msg(
                Message(toilet_id, MessageType.CLEAN)
            ),
        ),
        ending_program()
    )
    await run_sequence()


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
