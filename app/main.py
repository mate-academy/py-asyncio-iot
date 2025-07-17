import asyncio
from typing import Any, Awaitable
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)

async def main_async() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id = await service.register_device(hue_light)
    speaker_id = await service.register_device(speaker)
    toilet_id = await service.register_device(toilet)

    await run_sequence(
        run_parallel(
            service.send_message(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_message(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        service.send_message(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")),
    )

    await run_sequence(
        run_parallel(
            service.send_message(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_message(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        service.send_message(Message(toilet_id, MessageType.FLUSH)),
        service.send_message(Message(toilet_id, MessageType.CLEAN)),
    )

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    asyncio.run(main_async())
    end = time.perf_counter()
    print("Elapsed:", end - start)
