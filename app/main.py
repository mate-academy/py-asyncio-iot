import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


async def main() -> None:
    service = IOTService()

    light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    )

    print("\n--- Wake up program ---")
    await run_parallel(
        service.send_msg(Message(light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Never Gonna Give You Up"
                )
            )
        ),
    )

    print("\n--- Sleep program ---")
    await run_parallel(
        service.send_msg(Message(light_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        )
    )

    await asyncio.gather(
        service.unregister_device(light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
