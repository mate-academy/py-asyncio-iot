import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    # 1. Create an async IOT service instance
    service = IOTService()

    # 2. Instantiate our network-connected physical devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    print("===== PARALLEL DEVICE REGISTRATION =====")
    # Register all devices simultaneously using
    # asyncio.gather to capture unique keys
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )
    print("All devices successfully registered concurrently.\n")

    print("===== RUNNING WAKE UP PROGRAM =====")
    # Combined run logic replacing the legacy sequential wake_up_program array.
    # Constraints: Light switches on instantly,
    # while Speaker runs sequentially.
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(
                speaker_id,
                MessageType.SWITCH_ON
            )
            ),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            )
        )
    )
    print("===== END OF WAKE UP PROGRAM =====\n")

    print("===== RUNNING SLEEP PROGRAM =====")
    # Combined run logic replacing the legacy sequential sleep_program array.
    # Constraints: Light and Speaker switch off
    # simultaneously with Toilet routines.
    # The Toilet must maintain a strict sequence:
    # Flush completely FIRST, then Clean.
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        )
    )
    print("===== END OF SLEEP PROGRAM =====\n")

    print("===== PARALLEL DEVICE DISCONNECTION =====")
    # Clean up device registry tracking non-blockingly across the event loop
    await run_parallel(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id)
    )
    print("All connections closed safely.")


if __name__ == "__main__":
    # Wrap execution inside performance counters
    # to measure runtime gains for the PR screenshot
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print(f"\nElapsed execution time: {round(end - start, 4)} seconds")
