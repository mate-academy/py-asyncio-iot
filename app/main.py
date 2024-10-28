import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from iot.async_helper import run_sequence, run_parallel


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    device_list = [hue_light, speaker, toilet]
    def_list = [service.register_device(device) for device in device_list]
    hue_light_id, speaker_id, toilet_id = await run_parallel(*def_list)

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await run_sequence(
        run_parallel(
            service.send_msg(wake_up_program[0]),
            service.send_msg(wake_up_program[1])
        ),
        service.send_msg(wake_up_program[2])
    )

    await run_sequence(
        run_parallel(
            service.send_msg(sleep_program[0]),
            service.send_msg(sleep_program[1]),
            service.send_msg(sleep_program[2])
        ),
        service.send_msg(sleep_program[3])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
