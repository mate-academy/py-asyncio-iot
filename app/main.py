import time
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


async def main() -> None:
    # create an IOT service
    service = IOTService()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        *[
            service.register_device(HueLightDevice()),
            service.register_device(SmartSpeakerDevice()),
            service.register_device(SmartToiletDevice())
        ]
    )

    parallel_wake_up_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
    ]

    sequence_wake_up_program = [
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        )
    ]

    sequence_sleep_program = [
        service.send_msg(Message(toilet_id, MessageType.FLUSH))
    ]

    parallel_sleep_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN))

    ]

    await run_parallel(*parallel_wake_up_program)
    await run_sequence(*sequence_wake_up_program)

    await run_sequence(*sequence_sleep_program)
    await run_parallel(*parallel_sleep_program)

    await run_sequence()

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
