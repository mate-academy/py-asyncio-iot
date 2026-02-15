import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
from iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # register devices simultaneously
    await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # run wake_up program
    # - Hue Light SWITCH_ON can run in parallel with Speaker operations
    # - Speaker must SWITCH_ON before PLAY_SONG
    print("=====RUNNING PROGRAM======")
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_ON),
        run_sequence(
            speaker.send_message(MessageType.SWITCH_ON),
            speaker.send_message(
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            ),
        ),
    )
    print("=====END OF PROGRAM======")

    # run sleep program
    # - Hue Light SWITCH_OFF and Speaker SWITCH_OFF can run in parallel
    # - Toilet must FLUSH before CLEAN (sequence)
    # - All three groups can run in parallel
    print("=====RUNNING PROGRAM======")
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF),
        run_sequence(
            toilet.send_message(MessageType.FLUSH),
            toilet.send_message(MessageType.CLEAN),
        ),
    )
    print("=====END OF PROGRAM======")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)

