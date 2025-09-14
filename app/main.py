import asyncio
import time

from app.iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from app.iot.message import Message, MessageType
from app.iot.service import IOTService, run_parallel, run_sequence


async def main_async() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await service.register_devices(
        [hue_light, speaker, toilet]
    )

    # create a few programs
    print("\n--- Wake Up Program ---")
    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_message(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_message(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ),
        ),
    )
    print("\n--- Sleep Program ---")
    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_message(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_message(Message(toilet_id, MessageType.FLUSH)),
            service.send_message(Message(toilet_id, MessageType.CLEAN)),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main_async())
    end = time.perf_counter()

    print("Elapsed:", end - start)
