import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(functions: list[asyncio.Future]) -> None:
    for function in functions:
        await function


async def run_parallel(functions: list[asyncio.Future]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    devices = [hue_light, speaker, toilet]

    device_ids = await asyncio.gather(*(service.register_device(device) for device in devices))
    hue_light_id, speaker_id, toilet_id = device_ids

    # run the wake up programs
    await run_parallel([
        asyncio.create_task(service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON))),
        asyncio.create_task(service.send_msg(Message(speaker_id, MessageType.SWITCH_ON))),
    ])
    await run_sequence([
        asyncio.create_task(service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")))
    ])

    # run the sleep programs
    await run_parallel([
        asyncio.create_task(service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF))),
        asyncio.create_task(service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF))),
        asyncio.create_task(service.send_msg(Message(toilet_id, MessageType.FLUSH))),
    ])
    await run_sequence([
        asyncio.create_task(service.send_msg(Message(toilet_id, MessageType.CLEAN))),
    ])

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
