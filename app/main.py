import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


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
        service.register_device(toilet),
    )

    # Wake up program
    print("=====RUNNING WAKE UP PROGRAM======")
    # First turn on devices in parallel
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
    )
    # Then play music (must be after speaker is turned on)
    await service.send_msg(
        Message(
            speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        )
    )
    print("=====END OF WAKE UP PROGRAM======")

    # Sleep program
    print("=====RUNNING SLEEP PROGRAM======")
    # First turn off devices in parallel
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
    )
    # Then handle toilet operations in sequence
    await run_sequence(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )
    print("=====END OF SLEEP PROGRAM======")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
