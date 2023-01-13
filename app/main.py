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


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # register a few devices
    res = await asyncio.gather(
        * [
            service.register_device(device)
            for device in (
                HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()
            )
        ]
    )

    parallel = [
        Message(res[0], MessageType.SWITCH_OFF),
        Message(res[1], MessageType.SWITCH_OFF),
        Message(res[2], MessageType.FLUSH),
        Message(res[2], MessageType.CLEAN),
    ]

    # run the programs
    await run_parallel(
        *[
            service.run_program([message])
            for message in [
                Message(res[0], MessageType.SWITCH_ON),
                Message(res[1], MessageType.SWITCH_ON),
            ]
        ]
    )
    await run_sequence(
        service.run_program(
            [
                Message(
                    res[1],
                    MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
                ),

            ]
        )
    )
    await run_parallel(
        *[
            service.run_program([message])
            for message in parallel
        ]
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
