import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def main() -> None:
    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    reg_hue_light_id = service.register_device(hue_light)
    reg_speaker_id = service.register_device(speaker)
    reg_toilet_id = service.register_device(toilet)

    register_ids = await asyncio.gather(
        reg_hue_light_id, reg_speaker_id, reg_toilet_id
    )
    hue_light_id, speaker_id, toilet_id = register_ids

    wake_up_program = run_sequence(
        run_parallel(service.run_program([
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON)
        ])),
        run_sequence(service.run_program([
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up")
        ]))
    )

    sleep_program = run_sequence(
        run_parallel(
            service.run_program([
                Message(hue_light_id, MessageType.SWITCH_OFF),
                Message(speaker_id, MessageType.SWITCH_OFF)
            ])
        ),
        run_sequence(
            service.run_program([
                Message(toilet_id, MessageType.FLUSH),
                Message(toilet_id, MessageType.CLEAN)
            ])
        )
    )

    await asyncio.gather(wake_up_program, sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
