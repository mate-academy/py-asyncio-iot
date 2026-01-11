import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

import asyncio
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

    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(service.register_device(hue_light))
        t2 = tg.create_task(service.register_device(speaker))
        t3 = tg.create_task(service.register_device(toilet))

    hue_light_id = t1.result()
    speaker_id = t2.result()
    toilet_id = t3.result()

    print("====== Running programs ======")

    # create a few programs
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")),
        )
    )
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    )

    print("===== END OF PROGRAMS =====")

    # run the programs


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
