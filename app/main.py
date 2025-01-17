import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_parallel, run_sequence


WAKE_UP_SONG = "Rick Astley - Never Gonna Give You Up"


async def setup_devices(service: IOTService) -> tuple[str, str, str]:
    """Setup and register all devices."""
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    return await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )


async def run_wake_up_program(
    service: IOTService, hue_light_id: str, speaker_id: str
) -> None:
    """Run the wake-up program sequence."""
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                WAKE_UP_SONG,
            )
        ),
    )


async def run_sleep_program(
    service: IOTService,
    hue_light_id: str,
    speaker_id: str,
    toilet_id: str,
) -> None:
    """Run the sleep program sequence."""
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )


async def cleanup_devices(
    service: IOTService,
    hue_light_id: str,
    speaker_id: str,
    toilet_id: str,
) -> None:
    """Cleanup and unregister all devices."""
    await run_parallel(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


async def main() -> None:
    """Main program entry point."""
    service = IOTService()

    try:
        hue_light_id, speaker_id, toilet_id = await setup_devices(service)

        await run_wake_up_program(service, hue_light_id, speaker_id)
        await run_sleep_program(service, hue_light_id, speaker_id, toilet_id)

    finally:
        await cleanup_devices(service, hue_light_id, speaker_id, toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
