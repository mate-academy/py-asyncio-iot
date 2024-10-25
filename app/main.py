import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    device_task1 = asyncio.create_task(service.register_device(hue_light))
    device_task2 = asyncio.create_task(service.register_device(speaker))
    device_task3 = asyncio.create_task(service.register_device(toilet))

    await asyncio.gather(device_task1, device_task2, device_task3)

    wake_up_program = [
        Message(device_task1.result(), MessageType.SWITCH_ON),
        Message(device_task2.result(), MessageType.SWITCH_ON),
        Message(
            device_task3.result(),
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sleep_program = [
        Message(device_task1.result(), MessageType.SWITCH_OFF),
        Message(device_task2.result(), MessageType.SWITCH_OFF),
        Message(device_task3.result(), MessageType.FLUSH),
        Message(device_task3.result(), MessageType.CLEAN),
    ]

    # run the programs
    await service.run_sequence(*wake_up_program)
    await service.run_parallel(*sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
