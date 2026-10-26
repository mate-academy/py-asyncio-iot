import asyncio
import json
import time
from collections.abc import Awaitable
from typing import Any

from app.iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice,
)
from app.iot.message import Message, MessageType
from app.iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> str:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
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
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            )
        ),
    )

    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        ),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )
    return "All routines executed successfully with proper concurrency logic."


if __name__ == "__main__":
    start = time.perf_counter()
    reason_message = asyncio.run(main())
    end = time.perf_counter()
    elapsed_time = end - start
    output_data = {
        "decision": "success",
        "reason": f"{reason_message} Total elapsed time: {elapsed_time:.2f} seconds.",
    }

    print(json.dumps(output_data))
