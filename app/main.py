import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    registered_devices = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )
    hue_light_id, speaker_id, toilet_id = registered_devices

    hue_light_id_on = service.send_msg(
        Message(hue_light_id, MessageType.SWITCH_ON)
    )
    speaker_on = service.send_msg(
        Message(speaker_id, MessageType.SWITCH_ON)
    )
    speaker_play = service.send_msg(
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        )
    )

    hue_light_off = service.send_msg(
        Message(hue_light_id, MessageType.SWITCH_OFF)
    )
    speaker_off = service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF))
    toilet_flush = service.send_msg(Message(toilet_id, MessageType.FLUSH))
    toilet_clean = service.send_msg(Message(toilet_id, MessageType.CLEAN))

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    await run_sequence(
        run_parallel(hue_light_id_on, speaker_on),
        speaker_play
    )

    await run_parallel(
        hue_light_off,
        speaker_off,
        run_sequence(
            toilet_flush,
            toilet_clean
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
