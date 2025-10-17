# main.py
import time
import asyncio
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


# ---- helpers from the task ----
async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def send(service: IOTService, msg: Message) -> None:
    await service.send_msg(msg)


async def amain() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    await run_sequence(
        run_parallel(
            send(service, Message(hue_light_id, MessageType.SWITCH_ON)),
            send(service, Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        run_parallel(
            send(service, Message(speaker_id, MessageType.PLAY_SONG,
                                  "Rick Astley - Never Gonna Give You Up")),
        ),
    )

    await run_sequence(
        run_parallel(
            send(service, Message(hue_light_id, MessageType.SWITCH_OFF)),
            send(service, Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        run_sequence(
            send(service, Message(toilet_id, MessageType.FLUSH)),
            send(service, Message(toilet_id, MessageType.CLEAN)),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(amain())
    end = time.perf_counter()
    print("Elapsed:", end - start)
