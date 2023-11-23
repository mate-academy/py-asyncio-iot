import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices

    devices = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    )
    hue_light_id, speaker_id, toilet_id = devices

    # wake up programs

    await run_parallel(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_ON),
                Message(speaker_id, MessageType.SWITCH_ON),
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                ),
            ]
        ),
    )

    # sleep programs

    await run_parallel(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_OFF),
                Message(speaker_id, MessageType.SWITCH_OFF),
                Message(toilet_id, MessageType.FLUSH),
                Message(toilet_id, MessageType.CLEAN),
            ]
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
