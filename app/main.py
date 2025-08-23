import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


service = IOTService()


async def run_sequence(*messages: Awaitable[Any]) -> None:
    for message in messages:
        await service.send_msg(message)


async def run_parallel(*messages: Awaitable[Any]) -> None:
    await asyncio.gather(*(service.send_msg(message) for message in messages))


async def main() -> None:

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id_cor = asyncio.create_task(service.register_device(hue_light))
    speaker_id_cor = asyncio.create_task(service.register_device(speaker))
    toilet_id_cor = asyncio.create_task(service.register_device(toilet))

    hue_light_id = await hue_light_id_cor
    speaker_id = await speaker_id_cor
    toilet_id = await toilet_id_cor

    wake_up_program = [
        run_parallel(
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON)
        ),
        run_sequence(
            Message(
                speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            ),
        )
    ]

    sleep_program = [
        run_sequence(
            Message(toilet_id, MessageType.FLUSH),
            Message(toilet_id, MessageType.CLEAN),
            Message(speaker_id, MessageType.SWITCH_OFF),
            Message(hue_light_id, MessageType.SWITCH_OFF),
        )
    ]

    for program in wake_up_program:
        await program

    for program in sleep_program:
        await program


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
