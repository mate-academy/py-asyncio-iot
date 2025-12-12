import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    list_of_devices = [hue_light, speaker, toilet]
    ids = [service.register_device(device) for device in list_of_devices]
    results = await asyncio.gather(*ids)

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    await run_parallel(
        service.send_msg(Message(results[0], MessageType.SWITCH_ON)),
        service.send_msg(Message(results[1], MessageType.SWITCH_ON))
    )

    await run_sequence(
        service.send_msg(
            Message(results[1],
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up")
        ),
        service.send_msg(Message(results[2], MessageType.FLUSH)),
        service.send_msg(Message(results[2], MessageType.CLEAN))
    )

    await run_parallel(
        service.send_msg(Message(results[0], MessageType.SWITCH_OFF)),
        service.send_msg(Message(results[1], MessageType.SWITCH_OFF))
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
