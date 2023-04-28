import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.service import IOTService
from iot.message import Message, MessageType


async def main() -> None:
    # create an IOT service
    service = IOTService()
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    await service.run_sequence(
        *[
            service.run_program(
                [
                    Message(hue_light_id, MessageType.SWITCH_ON),
                    Message(speaker_id, MessageType.SWITCH_ON),
                    Message(
                        speaker_id,
                        MessageType.PLAY_SONG,
                        "Rick Astley - Never Gonna Give You Up"
                    ),
                ]
            )
        ],
        *[
            service.run_program(
                [
                    Message(hue_light_id, MessageType.SWITCH_OFF),
                    Message(speaker_id, MessageType.SWITCH_OFF),
                    Message(toilet_id, MessageType.FLUSH),
                    Message(toilet_id, MessageType.CLEAN),
                ]
            )
        ]
    )

    await asyncio.gather(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
