import asyncio
from collections.abc import Awaitable
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    print("===RUNNING SEQUENTIALLY===")
    for function in functions:
        await function
    print("===END RUNNING SEQUENTIALLY")


async def run_parallel(*functions: Awaitable[Any]) -> None:
    print("===RUNNING PARALLEL===")
    await asyncio.gather(*functions)
    print("===END RUNNING PARALLEL===")


async def main() -> None:
    service = IOTService()

    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()]
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )

    wake_up_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up",
                ),
            ),
        ),
    ]

    sleep_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        ),
    ]

    await run_parallel(*wake_up_program)
    await run_parallel(*sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
