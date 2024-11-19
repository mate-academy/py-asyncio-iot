import asyncio
import time
from typing import Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def connect(thing: Any, service: Any) -> str:
    thing_id = await service.register_device(thing)
    return thing_id


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()]
    connections = await asyncio.gather(*[connect(device, service) for device in devices])
    hue_light_id = connections[0]
    speaker_id = connections[1]
    toilet_id = connections[2]

    # create a few programs
    parallel_program_1 = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(toilet_id, MessageType.FLUSH),
    ]
    parallel_program_2 = [
        Message(toilet_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
        Message(toilet_id, MessageType.CLEAN),
    ]
    parallel_program_3 = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]
    sequence_program = [
        service.run_parallel(parallel_program_1),
        service.run_parallel(parallel_program_2),
        service.run_parallel(parallel_program_3)
    ]

    await service.run_sequence(sequence_program)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
