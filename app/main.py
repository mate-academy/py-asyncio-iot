import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


def async_program_state_decorator(func):
    async def wrapper(*args):
        print("=====RUNNING PROGRAM======")
        result = await func(*args)
        print("=====END OF PROGRAM======")
        return result
    return wrapper


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


@async_program_state_decorator
async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()


    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(device=hue_light),
        service.register_device(device=speaker),
        service.register_device(device=toilet),
    )

    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.run_program(
                [
                    Message(speaker_id, MessageType.SWITCH_ON),
                    Message(
                        speaker_id,
                        MessageType.PLAY_SONG,
                        "Rick Astley - Never Gonna Give You Up",
                    ),
                ]
            )
        ),
    )

    await run_parallel(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_OFF),
                Message(speaker_id, MessageType.SWITCH_OFF),
            ]
        ),
        run_sequence(
            service.run_program(
                [
                    Message(toilet_id, MessageType.FLUSH),
                    Message(toilet_id, MessageType.CLEAN),
                ]
            )
        ),
    )
    await asyncio.gather(
        hue_light.disconnect(),
        speaker.disconnect(),
        toilet.disconnect(),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
