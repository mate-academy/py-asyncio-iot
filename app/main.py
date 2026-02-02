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
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # Register devices concurrently
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(service.register_device(device))
            for device in (hue_light, speaker, toilet)
        ]

    hue_light_id = tasks[0].result()
    speaker_id = tasks[1].result()
    toilet_id = tasks[2].result()

    # -----------------------------
    # WAKE UP PROGRAM
    # -----------------------------
    # Speaker: SWITCH_ON → PLAY_SONG (sequence)
    speaker_sequence = run_sequence(
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        ),
    )

    # Light: SWITCH_ON (independent)
    light_on = service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON))

    # Run both groups in parallel
    await run_parallel(light_on, speaker_sequence)

    # -----------------------------
    # SLEEP PROGRAM
    # -----------------------------
    # Group 1: turn off devices (parallel)
    switch_off_parallel = run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
    )

    # Group 2: toilet cleaning cycle (sequence)
    toilet_sequence = run_sequence(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )

    # Run both groups in parallel (top-level)
    await run_parallel(switch_off_parallel, toilet_sequence)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
