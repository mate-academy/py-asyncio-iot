import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main():
    service = IOTService()

    ids = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice())
    )
    hue_light_id, smart_speaker_id, smart_toilet_id = ids

    await service.run_program(
        [
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(hue_light_id, MessageType.SWITCH_OFF),

            Message(smart_speaker_id, MessageType.SWITCH_ON),
            Message(smart_speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
            Message(smart_speaker_id, MessageType.SWITCH_OFF),

            Message(smart_toilet_id, MessageType.FLUSH),
            Message(smart_toilet_id, MessageType.CLEAN),
        ]
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
