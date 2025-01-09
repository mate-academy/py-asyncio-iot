import asyncio
import time
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)

async def main() -> None:
    # create an IOT service
    service = IOTService()

    hue_light, speaker, toilet = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice())
    )

    wake_up_messages = [
        Message(device_id=hue_light, msg_type=MessageType.SWITCH_ON),
        Message(device_id=speaker, msg_type=MessageType.SWITCH_ON),
        Message(device_id=speaker, msg_type=MessageType.PLAY_SONG, data="Rick Astley - Never Gonna Give You Up")
    ]

    sleep_messages = [
        Message(device_id=hue_light, msg_type=MessageType.SWITCH_OFF),
        Message(device_id=speaker, msg_type=MessageType.SWITCH_OFF),
        Message(device_id=toilet, msg_type=MessageType.FLUSH),
        Message(device_id=toilet, msg_type=MessageType.CLEAN)
    ]

    # Запускаємо програми
    await run_parallel(
        service.send_msg(wake_up_messages[0]),
        service.send_msg(wake_up_messages[1])
    )
    await run_sequence(
        service.send_msg(wake_up_messages[2])
    )

    await run_parallel(
        service.send_msg(sleep_messages[0]),
        service.send_msg(sleep_messages[1])
    )
    await run_sequence(
        service.send_msg(sleep_messages[2]),
        service.send_msg(sleep_messages[3])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
