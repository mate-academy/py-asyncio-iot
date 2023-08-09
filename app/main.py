import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    devices = {
        "hue_light": HueLightDevice(),
        "speaker": SmartSpeakerDevice(),
        "toilet": SmartToiletDevice()
    }
    devices_register = [service.register_device(devices[device])
                        for device in devices]
    hue_light_id, speaker_id, toilet_id, *_ = await asyncio.gather(
        *devices_register
    )

    await run_sequence(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_parallel(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"))
        )
    )
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
