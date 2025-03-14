import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # create and register a few devices
    async with asyncio.TaskGroup() as tg:
        hue_light_id = tg.create_task(service.register_device(hue_light))
        speaker_id = tg.create_task(service.register_device(speaker))
        toilet_id = tg.create_task(service.register_device(toilet))

    hue_light_id = hue_light_id.result()
    speaker_id = speaker_id.result()
    toilet_id = toilet_id.result()

    async def wake_up(service: IOTService, hue_light_id: str, speaker_id: str) -> None:
        await service.run_parallel([
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON),
        ])

        await service.run_sequence([
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        ])

    async def sleep(service: IOTService, hue_light_id: str, speaker_id: str, toilet_id: str) -> None:
        await service.run_parallel([
            Message(hue_light_id, MessageType.SWITCH_OFF),
            Message(speaker_id, MessageType.SWITCH_OFF),
        ])

        await service.run_sequence([
            Message(toilet_id, MessageType.FLUSH),
            Message(toilet_id, MessageType.CLEAN),
        ])

    await wake_up(service, hue_light_id, speaker_id)
    await sleep(service, hue_light_id, speaker_id, toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
