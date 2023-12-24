import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # create a few programs
    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    await run_sequence(
        run_parallel(
            service.get_device(hue_light_id).send_message(
                MessageType.SWITCH_ON,
            ),
            service.get_device(speaker_id).send_message(MessageType.SWITCH_ON),
            service.get_device(speaker_id).send_message(
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            ),
        ),
        run_parallel(
            service.get_device(hue_light_id).send_message(
                MessageType.SWITCH_OFF
            ),
            service.get_device(speaker_id).send_message(
                MessageType.SWITCH_OFF
            ),
            service.get_device(toilet_id).send_message(
                MessageType.FLUSH
            ),
            service.get_device(toilet_id).send_message(
                MessageType.CLEAN
            ),
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
