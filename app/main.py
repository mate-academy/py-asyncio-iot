import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for func in functions:
        await func


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


# Обгортка для синхронного виклику send_msg
def sync_send(service: IOTService, msg: Message) -> None:
    service.send_msg(msg)


async def async_send(service: IOTService, msg: Message, executor: ThreadPoolExecutor) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, sync_send, service, msg)


async def main_async():
    service = IOTService()
    executor = ThreadPoolExecutor()

    # Реєстрація пристроїв — синхронна
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    # Wake-up: вмикаємо лампу + колонку паралельно, потім грає музика
    await run_sequence(
        run_parallel(
            async_send(service, Message(hue_light_id, MessageType.SWITCH_ON), executor),
            async_send(service, Message(speaker_id, MessageType.SWITCH_ON), executor),
        ),
        async_send(service, Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"), executor),
    )

    # Sleep: вимикаємо лампу + колонку паралельно, потім flush → clean
    await run_sequence(
        run_parallel(
            async_send(service, Message(hue_light_id, MessageType.SWITCH_OFF), executor),
            async_send(service, Message(speaker_id, MessageType.SWITCH_OFF), executor),
        ),
        run_sequence(
            async_send(service, Message(toilet_id, MessageType.FLUSH), executor),
            async_send(service, Message(toilet_id, MessageType.CLEAN), executor),
        ),
    )

    executor.shutdown(wait=True)


def main():
    start = time.perf_counter()
    asyncio.run(main_async())
    end = time.perf_counter()
    print("Elapsed:", end - start)


if __name__ == "__main__":
    main()
