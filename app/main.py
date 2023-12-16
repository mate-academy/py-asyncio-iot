import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id = asyncio.create_task(service.register_device(hue_light))
    speaker_id = asyncio.create_task(service.register_device(speaker))
    toilet_id = asyncio.create_task(service.register_device(toilet))

    await hue_light_id
    await speaker_id
    await toilet_id

    await service.run_sequence(
        await service.run_parallel(
            [
                Message(hue_light_id.result(), MessageType.SWITCH_ON),
                Message(speaker_id.result(), MessageType.SWITCH_ON),
            ]
        ),
        [
            Message(speaker_id.result(), MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        ]
    )

    await service.run_sequence(
        await service.run_parallel(
            [
                Message(hue_light_id.result(), MessageType.SWITCH_OFF),
                Message(speaker_id.result(), MessageType.SWITCH_OFF),
                Message(toilet_id.result(), MessageType.FLUSH),
            ]
        ),
        [
            Message(toilet_id.result(), MessageType.CLEAN),
        ]
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
