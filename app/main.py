import time
import asyncio
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*funcs_to_exec: Awaitable[Any]) -> None:
    for function in funcs_to_exec:
        await function


async def run_parallel(*funcs_to_exec: Awaitable[Any]) -> None:
    await asyncio.gather(*funcs_to_exec)


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    devices = [hue_light, speaker, toilet]

    result = await asyncio.gather(
        *[
            service.register_device(device)
            for device in devices
        ]
    )

    hue_light_id, speaker_id, toilet_id = result

    await run_sequence(
        run_parallel(
            service.send_msg(
                Message(hue_light_id, MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_ON)
            )
        ),
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        )
    )

    await run_sequence(
        run_parallel(
            service.send_msg(
                Message(hue_light_id, MessageType.SWITCH_OFF)
            ),
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_OFF)
            ),
            service.send_msg(
                Message(toilet_id, MessageType.FLUSH)
            )
        ),
        service.send_msg(
            Message(toilet_id, MessageType.CLEAN)
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)