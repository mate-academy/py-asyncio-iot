import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def first(
    service: IOTService, hue_light_id: str, speaker_id: str
) -> None:
    await service.run_program(
        [
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON),
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            ),
        ]
    )


async def second(
    service: IOTService, hue_light_id: str, speaker_id: str, toilet_id: str
) -> None:
    await service.run_program(
        [
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
            Message(toilet_id, MessageType.FLUSH),
            Message(toilet_id, MessageType.CLEAN),
        ]
    )


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    devices = (HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice())
    devices_id = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )
    hue_light_id, speaker_id, toilet_id = devices_id

    # create tasks
    tasks = [
        asyncio.create_task(first(service, hue_light_id, speaker_id)),
        asyncio.create_task(
            second(service, hue_light_id, speaker_id, toilet_id)
        ),
    ]

    # wait for tasks to complete
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
