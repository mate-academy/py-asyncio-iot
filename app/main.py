import time
import asyncio
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


from typing import Any, Awaitable

async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    device_ids = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    )
    # create a few programs
    wake_up_program = [
        Message(device_ids[0], MessageType.SWITCH_ON),
        Message(device_ids[1], MessageType.SWITCH_ON),
        Message(device_ids[2], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(device_ids[0], MessageType.SWITCH_OFF),
        Message(device_ids[1], MessageType.SWITCH_OFF),
        Message(device_ids[2], MessageType.FLUSH),
        Message(device_ids[2], MessageType.CLEAN),
    ]

    tasks = []
    for msg in wake_up_program:
        task = asyncio.create_task(service.send_msg(msg))
        tasks.append(task)

    for msg in sleep_program:
        task = asyncio.create_task(service.send_msg(msg))
        tasks.append(task)

    # run the programs
    await asyncio.gather(*tasks)
    tasks = [
        service.unregister_device(device_ids[i]) for i in range(len(device_ids))
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
