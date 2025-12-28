import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


async def main() -> None:
    service = IOTService()
    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice(), ]

    devices_id = await asyncio.gather(
        *(service.register_device(device) for device in devices)
    )

    light_id, speaker_id, toilet_id = devices_id

    await run_parallel(
        service.send_msg(Message(light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up")
            )
        )
    )

    await run_parallel(
        service.send_msg(Message(light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
