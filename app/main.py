import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(service: IOTService, *messages):
    for msg in messages:
        await service.send_msg(msg)


async def run_parallel(service: IOTService, *messages):
    tasks = []
    for msg in messages:
        if isinstance(msg, list):
            tasks.append(run_sequence(service, *msg))
        else:
            tasks.append(service.send_msg(msg))
    await asyncio.gather(*tasks)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # create a few programs
    print("=====RUNNING WAKE-UP PROGRAM======")
    await run_parallel(
        service,
        Message(hue_light_id, MessageType.SWITCH_ON),
        [
            Message(speaker_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        ]
    )
    print("=====END OF WAKE-UP PROGRAM======")

    print("=====RUNNING SLEEP PROGRAM======")
    await run_parallel(
        service,
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        [
            Message(toilet_id, MessageType.FLUSH),
            Message(toilet_id, MessageType.CLEAN),
        ]
    )
    print("=====END OF SLEEP PROGRAM======")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
