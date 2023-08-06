import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


def create_program(*messages):
    return [Message(*msg) for msg in messages]


async def main() -> None:
    service = IOTService()

    devices = [
        HueLightDevice(),
        SmartSpeakerDevice(),
        SmartToiletDevice()
    ]

    tasks = [
        asyncio.create_task(
            service.register_device(
                device
            )
        )
        for device in devices
    ]

    list_of_id = await asyncio.gather(*tasks)

    hue_light_id, speaker_id, toilet_id = list_of_id

    wake_up_program = create_program(
        (hue_light_id, MessageType.SWITCH_ON),
        (speaker_id, MessageType.SWITCH_ON),
        (speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
    )

    sleep_program = create_program(
        (hue_light_id, MessageType.SWITCH_OFF),
        (speaker_id, MessageType.SWITCH_OFF),
        (toilet_id, MessageType.FLUSH),
        (toilet_id, MessageType.CLEAN)
    )

    await asyncio.gather(
        service.run_program(wake_up_program),
        service.run_program(sleep_program)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
