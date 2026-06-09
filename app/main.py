import time
import asyncio
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Виконує команди строго одна за одною."""
    for func in functions:
        await func


async def run_parallel(*functions: Awaitable[Any]) -> None:
    """Виконує всі команди одночасно."""
    async with asyncio.TaskGroup() as tg:
        for func in functions:
            tg.create_task(func)


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(service.register_device(hue_light))
        task2 = tg.create_task(service.register_device(speaker))
        task3 = tg.create_task(service.register_device(toilet))

    hue_light_id = task1.result()
    speaker_id = task2.result()
    toilet_id = task3.result()

    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON))
    )

    await run_sequence(
        service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
    )

    await run_sequence(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN))
    )

    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF))
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print(f"Elapsed: {end - start:.4f} seconds")