import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id = await service.register_device(hue_light)
    speaker_id = await service.register_device(speaker)
    toilet_id = await service.register_device(toilet)

    # create a few programs
    hue_light_sequence = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(hue_light_id, MessageType.SWITCH_OFF)
    ]
    speaker_sequence = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]
    toilet_sequence = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await run_parallel(
        *[
            run_sequence(
                *[service.send_msg(msg) for msg in seq]
            )
            for seq in (
                hue_light_sequence,
                speaker_sequence,
                toilet_sequence
            )
        ]
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
