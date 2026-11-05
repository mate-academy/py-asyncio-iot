import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices simultaneously (in parallel)
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # Wake-up program logic:
    # 1. Switch on light and speaker in parallel
    # 2. Play song on speaker
    print("=====RUNNING PROGRAM======")
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")),
    )
    print("=====END OF PROGRAM======")

    # Sleep program logic:
    # 1. Switch off light and speaker, flush toilet in parallel (or combine as needed)
    # 2. Clean toilet (must run after flush)
    print("=====RUNNING PROGRAM======")
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            run_sequence(
                service.send_msg(Message(toilet_id, MessageType.FLUSH)),
                service.send_msg(Message(toilet_id, MessageType.CLEAN)),
            ),
        )
    )
    print("=====END OF PROGRAM======")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)