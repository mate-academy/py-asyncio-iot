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
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        hue_light_id,
        speaker_id,
        toilet_id
    )

    # run the programs
    await run_parallel(
        service.run_program([Message(hue_light_id, MessageType.SWITCH_ON)]),
        run_sequence(
            *[
                service.run_program(
                    [Message(speaker_id, MessageType.SWITCH_ON)]),
                service.run_program(
                    [
                        Message(
                            speaker_id,
                            MessageType.PLAY_SONG,
                            "Rick Astley - Never Gonna Give You Up",
                        )
                    ]
                ),
            ]
        ),
    )

    await run_parallel(
        service.run_program([Message(hue_light_id, MessageType.SWITCH_OFF)]),
        service.run_program([Message(speaker_id, MessageType.SWITCH_OFF)]),
        run_sequence(
            service.run_program(
                [
                    Message(toilet_id, MessageType.FLUSH),
                    Message(toilet_id, MessageType.CLEAN),
                ]
            )
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
