import asyncio
import time
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_wake_up_program(service: IOTService, hue_light_id: str, speaker_id: str) -> None:
    # Create tasks for concurrent operations
    tasks = [
        asyncio.create_task(service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON))),
        asyncio.create_task(service.send_msg(Message(speaker_id, MessageType.SWITCH_ON))),
    ]
    # Wait for the switch on commands to complete before starting the song
    await asyncio.gather(*tasks)

    # Play song after both switch on commands are done
    await service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))


async def run_sleep_program(service: IOTService, hue_light_id: str, speaker_id: str, toilet_id: str) -> None:
    # Create tasks for concurrent operations
    tasks = [
        asyncio.create_task(service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF))),
        asyncio.create_task(service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF))),
    ]
    # Wait for the switch off commands to complete before flushing and cleaning
    await asyncio.gather(*tasks)

    # Flush and clean sequentially
    await asyncio.gather(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # Register devices and handle disconnection in a finally block
    try:
        hue_light_id = await service.register_device(hue_light)
        speaker_id = await service.register_device(speaker)
        toilet_id = await service.register_device(toilet)

        # run the programs
        await run_wake_up_program(service, hue_light_id, speaker_id)
        await run_sleep_program(service, hue_light_id, speaker_id, toilet_id)

    finally:
        # Ensure devices are disconnected
        await service.unregister_device(hue_light_id)
        await service.unregister_device(speaker_id)
        await service.unregister_device(toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
