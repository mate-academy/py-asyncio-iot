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
    devices = await asyncio.gather(
        *[
            service.register_device(device)
            for device in (hue_light, speaker, toilet)
        ]
    )
    hue_light_id, speaker_id, toilet_id = devices

    program_smart_hue_light = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(hue_light_id, MessageType.SWITCH_OFF),
    ]

    program_smart_speaker = [
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up",
        ),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]

    program_smart_toilet = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run smart devices programs
    await asyncio.gather(
        *[
            service.run_program(program)
            for program in (
                program_smart_hue_light,
                program_smart_speaker,
                program_smart_toilet,
            )
        ]
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
