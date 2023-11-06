import time
import asyncio
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    async with asyncio.TaskGroup() as tg:
        hue_light_id = tg.create_task(service.register_device(hue_light))
        speaker_id = tg.create_task(service.register_device(speaker))
        toilet_id = tg.create_task(service.register_device(toilet))

    await run_sequence(
        service.send_msg(
            Message(hue_light_id.result(), MessageType.SWITCH_ON)
        ),
        run_parallel(
            service.send_msg(
                Message(speaker_id.result(), MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(
                    speaker_id.result(),
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up",
                )
            ),
        ),
    )

    await run_parallel(
        service.send_msg(
            Message(hue_light_id.result(), MessageType.SWITCH_OFF)
        ),
        service.send_msg(Message(speaker_id.result(), MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id.result(), MessageType.FLUSH)),
            service.send_msg(Message(toilet_id.result(), MessageType.CLEAN)),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
