import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    gather = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )
    hue_light_id, speaker_id, toilet_id = gather

    speaker_sequence_program = [
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]
    hue_light_sequence_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(hue_light_id, MessageType.SWITCH_OFF),
    ]
    toilet_sequence_program = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]
    parallel_sequence_program = [
        speaker_sequence_program,
        hue_light_sequence_program,
        toilet_sequence_program
    ]

    await service.run_parallel(parallel_sequence_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
