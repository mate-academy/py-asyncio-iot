import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    connections = await asyncio.gather(
        *[
            service.register_device(device)
            for device in [
                HueLightDevice(),
                SmartSpeakerDevice(),
                SmartToiletDevice(),
            ]
        ]
    )
    hue_light_id, toilet_id, speaker_id = connections

    # create a few programs
    parallel_1 = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(toilet_id, MessageType.FLUSH),
    ]

    parallel_2 = [
        Message(
            toilet_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up",
        ),
        Message(toilet_id, MessageType.CLEAN),
    ]

    parallel_3 = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        ]

    # run the programs
    await service.run_sequence(
        [
            service.run_parallel(parallel_1),
            service.run_parallel(parallel_2),
            service.run_parallel(parallel_3),
        ]
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
