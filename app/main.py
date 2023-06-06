import time
import asyncio
from typing import Any, Awaitable, List

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> List[Any]:
    return await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # create a few programs
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(
                speaker_id, MessageType.PLAY_SONG,
                "Nirvana - Smells Like Teen Spirit"
            )),
        )
    )

    # sleep_program
    await run_parallel(
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
