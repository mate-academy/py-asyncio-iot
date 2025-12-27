import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices

    devices = [
        HueLightDevice(),
        SmartSpeakerDevice(),
        SmartToiletDevice()
    ]

    device_ids = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )

    hue_light_id, speaker_id, toilet_id = device_ids

    await service.run_parallel([
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ])

    await service.run_sequence([
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        )
    ])

    await asyncio.gather(
        service.run_parallel([
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
        ]),
        service.run_sequence([
            Message(toilet_id, MessageType.FLUSH),
            Message(toilet_id, MessageType.CLEAN),
        ])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
