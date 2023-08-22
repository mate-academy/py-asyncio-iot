import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def register_devices(service, devices):
    ids = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )
    return ids


async def run_programs(service, programs):
    await asyncio.gather(
        *[service.run_program(program) for program in programs]
    )


async def async_main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()]

    device_ids = await register_devices(service, devices)

    # create a few programs
    wake_up_program = [
        Message(device_ids[0], MessageType.SWITCH_ON),
        Message(device_ids[1], MessageType.SWITCH_ON),
        Message(device_ids[1], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(device_ids[0], MessageType.SWITCH_OFF),
        Message(device_ids[1], MessageType.SWITCH_OFF),
        Message(device_ids[2], MessageType.FLUSH),
        Message(device_ids[2], MessageType.CLEAN),
    ]

    # run the programs
    await run_programs(service, [wake_up_program, sleep_program])


if __name__ == "__main__":
    start = time.perf_counter()

    asyncio.run(async_main())

    end = time.perf_counter()

    print("Elapsed:", end - start)
