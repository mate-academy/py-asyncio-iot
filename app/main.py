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
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        *[
            service.register_device(hue_light),
            service.register_device(speaker),
            service.register_device(toilet),
        ]
    )

    wake_up_program_parallel = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]

    wake_up_program_sequence = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up",
        ),
    ]

    sleep_program_parallel = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
    ]

    sleep_program_sequence = [
        Message(toilet_id, MessageType.CLEAN),
    ]

    await service.run_program(
        wake_up_program_parallel, wake_up_program_sequence
    )
    await service.run_program(sleep_program_parallel, sleep_program_sequence)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
