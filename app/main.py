import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
from iot.service import IOTService

from iot.helpers import run_parallel, run_sequence


async def main() -> None:
    start_time = time.perf_counter()

    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    await run_sequence(
        run_parallel(
            service.send_message(hue_light_id, MessageType.SWITCH_ON),
            service.send_message(speaker_id, MessageType.SWITCH_ON),
        ),
        service.send_message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up",
        ),
    )

    await run_sequence(
        service.send_message(toilet_id, MessageType.FLUSH),
        service.send_message(toilet_id, MessageType.CLEAN),
        run_parallel(
            service.send_message(hue_light_id, MessageType.SWITCH_OFF),
            service.send_message(speaker_id, MessageType.SWITCH_OFF),
        ),
    )

    end_time = time.perf_counter()
    print(f"\nElapsed time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())