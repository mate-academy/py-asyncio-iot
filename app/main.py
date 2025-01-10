import asyncio
import time
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: asyncio.Future) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: asyncio.Future) -> None:

    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id = await service.register_device(hue_light)
    speaker_id = await service.register_device(speaker)
    toilet_id = await service.register_device(toilet)

    wake_up_program = [
        asyncio.create_task(service.send_msg(
            Message(hue_light_id, MessageType.SWITCH_ON)
        )),
        asyncio.create_task(service.send_msg(
            Message(speaker_id, MessageType.SWITCH_ON)
        )),
    ]
    await run_parallel(*wake_up_program)

    await service.send_msg(
        Message(speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up")
    )

    sleep_program = [
        asyncio.create_task(service.send_msg(
            Message(hue_light_id, MessageType.SWITCH_OFF)
        )),
        asyncio.create_task(service.send_msg(
            Message(speaker_id, MessageType.SWITCH_OFF)
        )),
    ]
    await run_parallel(*sleep_program)

    await run_sequence(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN))
    )

if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed: {elapsed_time: .2f} seconds")
