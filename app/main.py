import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> list:
    return await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    async def register(dev) -> str:
        return service.register_device(dev)

    ids = await run_parallel(
        register(hue_light),
        register(speaker),
        register(toilet),
    )
    hue_light_id, speaker_id, toilet_id = ids

    print("\n--- Wake up program ---")

    async def run(messages) -> None:
        return service.run_program(messages)

    await run_sequence(
        run_parallel(
            run([Message(hue_light_id, MessageType.SWITCH_ON)]),
            run([Message(speaker_id, MessageType.SWITCH_ON)]),
        ),
        run([
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
        ]),
    )

    print("\n--- Sleep program ---")
    await run_parallel(
        run_sequence(
            run([Message(toilet_id, MessageType.FLUSH)]),
            run([Message(toilet_id, MessageType.CLEAN)]),
        ),
        run_parallel(
            run([Message(hue_light_id, MessageType.SWITCH_OFF)]),
            run([Message(speaker_id, MessageType.SWITCH_OFF)]),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
