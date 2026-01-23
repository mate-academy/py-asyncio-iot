import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
from iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # WAKE UP
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

    # SLEEP
    await run_sequence(
        run_parallel(
            service.send_message(hue_light_id, MessageType.SWITCH_OFF),
            service.send_message(speaker_id, MessageType.SWITCH_OFF),
        ),
        service.send_message(toilet_id, MessageType.FLUSH),
        service.send_message(toilet_id, MessageType.CLEAN),
    )

    await run_parallel(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    print("Elapsed:", time.perf_counter() - start)



