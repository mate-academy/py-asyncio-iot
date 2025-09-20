from typing import Any, Awaitable
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> Any:
    return await asyncio.gather(*functions)

async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )


    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_message(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_message(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
        ),
        run_sequence(
           service.send_message(Message(toilet_id, MessageType.FLUSH)),
            service.send_message(Message(toilet_id, MessageType.CLEAN))
        )
    )

    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_message(Message(speaker_id, MessageType.SWITCH_OFF)),
    )


if __name__ == "__main__":
    import time
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
