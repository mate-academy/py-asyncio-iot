import asyncio
import time

from iot.utils import run_sequence, run_parallel
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
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # compound instructions
    startup_instructions = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
    ]
    work_instructions = [
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        )
    ]
    shutdown_instructions = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
    ]
    toilet_instructions = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    get_program = (
        lambda instructions: [service.send_msg(msg) for msg in instructions]
    )

    # run the program instructions
    print("=====RUNNING PROGRAM======")
    await run_sequence(
        run_parallel(*get_program(startup_instructions)),
        run_parallel(*get_program(work_instructions)),
        run_parallel(*get_program(shutdown_instructions)),
        run_sequence(*get_program(toilet_instructions))
    )
    print("=====END OF PROGRAM======")

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
