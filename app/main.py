import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from iot.helpers import run_sequence, run_parallel


async def main() -> None:
    service = IOTService()

    # Create and register devices asynchronously
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    device_ids = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )
    hue_light_id, speaker_id, toilet_id = device_ids

    # Define wake-up program
    async def wake_up_program():
        await run_sequence(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        )
        await service.send_msg(
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
        )

    # Define sleep program
    async def sleep_program():
        await run_parallel(
            run_sequence(
                service.send_msg(Message(toilet_id, MessageType.FLUSH)),
                service.send_msg(Message(toilet_id, MessageType.CLEAN)),
            ),
            run_sequence(
                service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
                service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            ),
        )

    # Run the programs
    print("Running Wake-Up Program")
    await wake_up_program()
    print("Running Sleep Program")
    await sleep_program()


if __name__ == "__main__":
    import time

    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
