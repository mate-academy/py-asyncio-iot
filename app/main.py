import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable

async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)

async def main() -> None:
    service = IOTService()

    hue_light, speaker, toilet = HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    await run_sequence(
        run_parallel(
            service.send_msg(wake_up_program[0]),
            service.send_msg(wake_up_program[1])
        ),
        service.send_msg(wake_up_program[2])
    )

    await run_sequence(
        run_parallel(
            service.send_msg(sleep_program[0]),
            service.send_msg(sleep_program[1])
        ),
        run_sequence(
            service.send_msg(sleep_program[2]),
            service.send_msg(sleep_program[3])
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
