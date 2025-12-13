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
    tasks = [
        asyncio.create_task(service.register_device(task))
        for task in (hue_light, speaker, toilet)
    ]
    await asyncio.gather(*tasks)
    hue_light_id, speaker_id, toilet_id = tasks
    (hue_light_id,
     speaker_id,
     toilet_id) = (hue_light_id.result(),
                   speaker_id.result(),
                   toilet_id.result())

    turning_on_devices = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]

    play_song = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    turning_of_devices = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]

    toilet_cleaning = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN)
    ]

    async def run_parallel(messages: list[Message]) -> None:
        tasks = [
            asyncio.create_task(service.send_msg(msg)) for msg in messages
        ]
        await asyncio.gather(*tasks)

    async def run_sequence(messages: list[Message]) -> None:
        for msg in messages:
            await service.send_msg(msg)

    await asyncio.create_task(run_parallel(turning_on_devices))
    await asyncio.create_task(run_sequence(play_song))
    await asyncio.create_task(run_parallel(turning_of_devices))
    await asyncio.create_task(run_sequence(toilet_cleaning))

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
