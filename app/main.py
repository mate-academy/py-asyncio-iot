import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
import asyncio


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id = asyncio.create_task(
        service.register_device(hue_light)
    )
    speaker_id = asyncio.create_task(
        service.register_device(speaker)
    )
    toilet_id = asyncio.create_task(
        service.register_device(toilet)
    )

    await asyncio.gather(hue_light_id, speaker_id, toilet_id)
    # create a few programs
    wake_up_program_parallel = [
        Message(hue_light_id.result(), MessageType.SWITCH_ON),
        Message(speaker_id.result(), MessageType.SWITCH_ON),
    ]
    wake_up_program = [
        Message(speaker_id.result(), MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program_parallel = [
        Message(hue_light_id.result(), MessageType.SWITCH_OFF),
        Message(speaker_id.result(), MessageType.SWITCH_OFF),
    ]
    sleep_program = [
        Message(toilet_id.result(), MessageType.FLUSH),
        Message(toilet_id.result(), MessageType.CLEAN),
    ]

    await asyncio.create_task(service.run_program(wake_up_program_parallel, parallel=True))
    await asyncio.create_task(service.run_program(wake_up_program))

    await asyncio.create_task(
        service.run_program(sleep_program_parallel)
    )
    await asyncio.create_task(
        service.run_program(sleep_program)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
