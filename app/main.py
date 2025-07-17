import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


async def main() -> None:
    # Create IOT service
    service = IOTService()

    # Create devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # Register devices concurrently
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # Wake up program with logical sequencing
    print("\n===== RUNNING WAKE UP PROGRAM =====\n")
    await run_sequence(
        # Turn on devices in parallel
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        # Then play song
        service.send_msg(Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        )),
    )
    print("\n===== END OF WAKE UP PROGRAM =====\n")

    # Sleep program with logical sequencing
    print("\n===== RUNNING SLEEP PROGRAM =====\n")
    await run_parallel(
        # Turn off devices in parallel
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        # Toilet operations in sequence
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        ),
    )
    print("\n===== END OF SLEEP PROGRAM =====\n")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Total Elapsed Time:", end - start)
