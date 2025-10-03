import time
import asyncio

from iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice,
    run_parallel,
    run_sequence
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

    registration_tasks = [
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    ]

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(*registration_tasks)

    await run_parallel(
        run_sequence(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
        ),
        service.send_msg(Message(toilet_id, MessageType.PREHEAT))
    )

    await run_parallel(
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        ),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
    )

    unregistration_tasks = [
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    ]
    await asyncio.gather(*unregistration_tasks)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
