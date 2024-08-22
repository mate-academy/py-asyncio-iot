import asyncio
import time
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

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # create a few programs
    # wake_up program messages
    wake_up_light_on = Message(hue_light_id, MessageType.SWITCH_ON)
    wake_up_speaker_on = Message(speaker_id, MessageType.SWITCH_ON)
    wake_up_play_music = Message(
        speaker_id,
        MessageType.PLAY_SONG,
        "Rick Astley - Never Gonna Give You Up"
    )
    # sleep program messages
    sleep_light_off = Message(hue_light_id, MessageType.SWITCH_OFF)
    sleep_speaker_off = Message(speaker_id, MessageType.SWITCH_OFF)
    sleep_toilet_flush = Message(toilet_id, MessageType.FLUSH)
    sleep_toilet_clean = Message(toilet_id, MessageType.CLEAN)

    # run the programs
    await run_sequence(
        run_parallel(
            service.send_msg(wake_up_light_on),
            service.send_msg(wake_up_speaker_on)
        ),
        service.send_msg(wake_up_play_music)
    )

    await run_parallel(
        service.send_msg(sleep_light_off),
        service.send_msg(sleep_speaker_off),
        run_sequence(
            service.send_msg(sleep_toilet_flush),
            service.send_msg(sleep_toilet_clean),
        )
    )

    await run_parallel(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
