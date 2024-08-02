import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id = await service.register_device(hue_light)
    speaker_id = await service.register_device(speaker)
    toilet_id = await service.register_device(toilet)

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON, "Lite on"),
        Message(speaker_id, MessageType.SWITCH_ON, "Speaker on"),
        Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF, "Light off"),
        Message(speaker_id, MessageType.SWITCH_OFF, "Speaker off"),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    # run the programs
    await run_sequence(
        service.send_msg(wake_up_program[0]),
        run_parallel(
            service.send_msg(wake_up_program[1]),
            service.send_msg(wake_up_program[2]),
        ),
    )

    await run_sequence(
        service.send_msg(sleep_program[0]),
        run_parallel(
            service.send_msg(sleep_program[1]),
            run_sequence(
                service.send_msg(sleep_program[2]),
                service.send_msg(sleep_program[3]),
            ),
        ),
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
