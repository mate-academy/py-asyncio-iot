import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType
from iot.service import IOTService
from iot.async_helper import run_parallel, run_sequence


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # register devices
    await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    # wake up program
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_ON),
        run_sequence(
            speaker.send_message(MessageType.SWITCH_ON),
            speaker.send_message(
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        )
    )

    # sleep program
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF),
        run_sequence(
            toilet.send_message(MessageType.FLUSH),
            toilet.send_message(MessageType.CLEAN)
        )
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
