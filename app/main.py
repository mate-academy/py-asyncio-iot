import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions) -> None:
    for function in functions:
        await function


async def run_parallel(*functions) -> None:
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
    switch_on_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON)
    ]
    play_song_program = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        )
    ]
    switch_off_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF)
    ]
    flush_toilet_program = [
        Message(toilet_id, MessageType.FLUSH)
    ]
    clean_toilet_program = [
        Message(toilet_id, MessageType.CLEAN)
    ]

    # run the programs
    # wake_up_program
    await run_sequence(
        service.run_program(switch_on_program),
        service.run_program(play_song_program),
    )

    # sleep_program
    await run_sequence(
        run_parallel(
            service.run_program(switch_off_program),
            service.run_program(flush_toilet_program)
        ),
        service.run_program(clean_toilet_program)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
