import time
import asyncio
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light, speaker, toilet = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice())
    )

    wake_up = run_sequence(
        run_parallel(
            service.send_msg(hue_light, MessageType.SWITCH_ON),
            service.send_msg(speaker, MessageType.SWITCH_ON)
        ),
        service.send_msg(speaker, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
    )

    sleep = run_sequence(
        run_parallel(
            service.send_msg(hue_light, MessageType.SWITCH_OFF),
            service.send_msg(speaker, MessageType.SWITCH_OFF)
        ),
        service.send_msg(toilet, MessageType.FLUSH),
        service.send_msg(toilet, MessageType.CLEAN)
    )

    # run the programs.
    await service.run_program(run_parallel(wake_up, sleep))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
