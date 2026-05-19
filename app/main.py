import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    devices_ids = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # create a few programs
    wake_up_program = [
        (
            Message(devices_ids[0], MessageType.SWITCH_ON),
            Message(devices_ids[1], MessageType.SWITCH_ON),
        ),
        Message(
            devices_ids[1],
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up",
        ),
    ]

    sleep_program = [
        (
            Message(devices_ids[0], MessageType.SWITCH_OFF),
            Message(devices_ids[1], MessageType.SWITCH_OFF),
        ),
        Message(devices_ids[2], MessageType.FLUSH),
        Message(devices_ids[2], MessageType.CLEAN),
    ]

    # run the programs
    await service.run_program(wake_up_program)
    await service.run_program(sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
