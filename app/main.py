import time

from app.iot.devices import HueLightDevice, SmartSpeakerDevice
from app.iot.devices import SmartToiletDevice
from app.iot.message import Message, MessageType
from app.iot.service import IOTService

import asyncio


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    # hue_light_id, speaker_id, toilet_id = await asyncio.gather(
    #     service.register_device(hue_light),
    #     service.register_device(speaker),
    #     service.register_device(toilet)
    # )
    hue_light_task = asyncio.create_task(service.register_device(hue_light))
    speaker_task = asyncio.create_task(service.register_device(speaker))
    toilet_task = asyncio.create_task(service.register_device(toilet))

    hue_light_id = await hue_light_task
    speaker_id = await speaker_task
    toilet_id = await toilet_task

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - "
                                                   "Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await service.run_program(wake_up_program)
    await service.run_program(sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
