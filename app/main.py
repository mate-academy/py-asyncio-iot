import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    device_ids = await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )
    hue_light_id, speaker_id, toilet_id = device_ids

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await run_parallel(
        service.send_msg(wake_up_program[0]),
        service.send_msg(wake_up_program[1]),
    )
    await run_sequence(service.send_msg(wake_up_program[2]))

    await run_parallel(
        service.send_msg(sleep_program[0]),
        service.send_msg(sleep_program[1]),
    )
    await run_sequence(
        service.send_msg(sleep_program[2]),
        service.send_msg(sleep_program[3])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
