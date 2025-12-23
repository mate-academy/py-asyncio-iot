import time
import asyncio

from app.iot.enums import RunTypeEnum
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    # It cannot be async (init)
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    tasks = [
        asyncio.create_task(service.register_device(hue_light)),
        asyncio.create_task(service.register_device(speaker)),
        asyncio.create_task(service.register_device(toilet)),
    ]

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(*tasks, return_exceptions=True)

    # Wake up
    # Parallel
    await service.run_program([
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ],
        RunTypeEnum.PARALLEL
    )
    # Sequential
    await service.run_program([Message(
        speaker_id,
        MessageType.PLAY_SONG,
        "Rick Astley - Never Gonna Give You Up")
    ],
        RunTypeEnum.SEQUENTIAL
    )

    # Sleep
    # Parallel
    await service.run_program(
        [
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
        ],
        RunTypeEnum.PARALLEL
    )
    await service.run_program([

        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ],
        RunTypeEnum.SEQUENTIAL
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
