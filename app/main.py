import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions):
    for function in functions:
        await function


async def run_parallel(*functions):
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    wake_up_tasks = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sleep_tasks = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    await run_parallel(
        service.send_message(wake_up_tasks[0]),
        service.send_message(wake_up_tasks[1]),
    )
    await service.send_message(wake_up_tasks[2])

    await run_parallel(
        service.send_message(sleep_tasks[0]),
        service.send_message(sleep_tasks[1]),
    )
    await run_sequence(
        service.send_message(sleep_tasks[2]),
        service.send_message(sleep_tasks[3]),
    )


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()

    print("Elapsed:", end_time - start_time)
