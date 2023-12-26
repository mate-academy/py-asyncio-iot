import time
import asyncio

from iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice
)
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # Wake up
    program_wake_up_parallel = [
        Message(hue_light_id, MessageType.SWITCH_ON),
    ]
    program_wake_up_sequence = [
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id,
            MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
    ]
    await service.run_program(
        program_wake_up_parallel,
        program_wake_up_sequence
    )

    # Sleep
    program_sleep_parallel = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]
    program_sleep_sequence = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]
    await service.run_program(
        program_sleep_parallel,
        program_sleep_sequence
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
