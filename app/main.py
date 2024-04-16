import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(
            *functions: Awaitable[Any]
    ) -> tuple[Awaitable[Any]]:
        return await asyncio.gather(*functions)

    [hue_light_id, speaker_id, toilet_id] = await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]

    actions_program = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
        Message(toilet_id, MessageType.FLUSH),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.CLEAN),
    ]

    await run_sequence(
        run_parallel(service.run_program(wake_up_program)),
        run_parallel(service.run_program(actions_program)),
        run_parallel(service.run_program(sleep_program))
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
