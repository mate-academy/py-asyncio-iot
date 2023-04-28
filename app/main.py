import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()
    devices = (HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice())
    devices_ids = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )

    hue_light_id = devices_ids[0]
    smart_speaker_id = devices_ids[1]
    smart_toilet_id = devices_ids[2]

    await service.run_program(
        [
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(smart_speaker_id, MessageType.SWITCH_ON),
            Message(
                smart_speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            ),
        ]
    )
    await service.run_program(
        [
            Message(hue_light_id, MessageType.SWITCH_OFF),
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
