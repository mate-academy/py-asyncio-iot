import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    devices = (HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice())

    registered_devices = await asyncio.gather(
        *[
            service.register_device(device)
            for device in devices
        ]
    )
    hue_light_id, speaker_id, toilet_id = registered_devices

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    await run_parallel(
            service.run_program(
                [
                    Message(
                        hue_light_id,
                        MessageType.SWITCH_ON,
                    ),
                    Message(
                        speaker_id,
                        MessageType.SWITCH_ON,
                    ),
                    Message(
                        speaker_id,
                        MessageType.PLAY_SONG,
                        "Rick Astley - Never Gonna Give You Up",
                    )
                ]
            )
        ),

    await run_sequence(
            service.run_program(
                [
                    Message(
                        hue_light_id,
                        MessageType.SWITCH_OFF,
                    ),
                    Message(
                        speaker_id,
                        MessageType.SWITCH_OFF,
                    ),
                    Message(
                        toilet_id,
                        MessageType.FLUSH,
                    ),
                    Message(
                        toilet_id,
                        MessageType.CLEAN,
                    )
                ]
            )
        )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
