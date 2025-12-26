import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # register devices in parallel
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # Wake up program - run in parallel where possible
    await service.run_sequence(
        # First turn on devices in parallel
        service.run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON))
        ),
        # Then play the song
        await service.send_msg(Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ))
    )

    # Sleep program - ensure proper sequencing
    await service.run_sequence(
        # First flush
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        # Then clean in parallel with turning off other devices
        service.run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print(f"Elapsed: {end - start:.2f} seconds")  # noqa: E231
