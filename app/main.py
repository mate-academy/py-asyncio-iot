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


async def async_register_device(service: IOTService, device) -> str:
    await asyncio.sleep(0)
    return service.register_device(device)


async def async_run_program(service: IOTService, program: list[Message]) -> None:
    await asyncio.sleep(0)
    service.run_program(program)


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    print("\n--- Registering devices ---")
    ids = await run_parallel(
        async_register_device(service, hue_light),
        async_register_device(service, speaker),
        async_register_device(service, toilet),
    )
    hue_light_id, speaker_id, toilet_id = ids
    print(f"Registered IDs: Hue={hue_light_id}, Speaker={speaker_id}, Toilet={toilet_id}")

    print("\n--- Wake up program ---")
    await run_sequence(
        run_parallel(
            async_run_program(service, [Message(hue_light_id, MessageType.SWITCH_ON)]),
            async_run_program(service, [Message(speaker_id, MessageType.SWITCH_ON)]),
        ),
        async_run_program(service, [
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
        ]),
    )

    print("\n--- Sleep program ---")
    await run_parallel(
        run_sequence(
            async_run_program(service, [Message(toilet_id, MessageType.FLUSH)]),
            async_run_program(service, [Message(toilet_id, MessageType.CLEAN)]),
        ),
        run_parallel(
            async_run_program(service, [Message(hue_light_id, MessageType.SWITCH_OFF)]),
            async_run_program(service, [Message(speaker_id, MessageType.SWITCH_OFF)]),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"\nElapsed time: {end - start:.2f} seconds")
