import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id = asyncio.create_task(service.register_device(hue_light))
    speaker_id = asyncio.create_task(service.register_device(speaker))
    toilet_id = asyncio.create_task(service.register_device(toilet))
    await run_parallel(hue_light_id, speaker_id, toilet_id)

    wake_and_sleep_program = [
        run_sequence(service.run_program([Message(hue_light_id.result(), MessageType.SWITCH_ON),
                                          Message(hue_light_id.result(), MessageType.SWITCH_OFF)])),
        run_sequence(service.run_program([Message(speaker_id.result(), MessageType.SWITCH_ON),
                                          Message(speaker_id.result(), MessageType.PLAY_SONG,
                                                  "Rick Astley - Never Gonna Give You Up"),
                                          Message(speaker_id.result(), MessageType.SWITCH_ON),
                                          Message(speaker_id.result(), MessageType.SWITCH_OFF)]),
                     ),
        run_sequence(service.run_program([
            Message(toilet_id.result(), MessageType.FLUSH),
            Message(toilet_id.result(), MessageType.CLEAN),
        ]))
    ]

    # run the programs
    await run_parallel(*wake_and_sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
