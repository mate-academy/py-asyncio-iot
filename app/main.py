import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for func in functions:
        await func


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main_async():
    service = IOTService()

    # створення девайсів
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # sync реєстрація
    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    # Wake-up логіка: вмикання світла і колонки паралельно, потім музика
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
    )

    # Sleep логіка: вимкнення світла і колонки паралельно, потім flush → clean
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    )


def main():
    start = time.perf_counter()
    asyncio.run(main_async())
    end = time.perf_counter()
    print(f"Elapsed: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
