import time
from typing import Awaitable, Any

import asyncio

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

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice())
    )

    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        # Can't play song if speaker it turned off,
        # but flush can be paralleled with playback
        run_parallel(
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ),
            service.send_msg(Message(toilet_id, MessageType.FLUSH))
        ),
        run_parallel(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        )
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
