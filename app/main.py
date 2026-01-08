import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # create a few programs
    async def wake_up_program(hue_light_id: str, speaker_id: str) -> None:
        await service.run_parallel(
            [
                Message(hue_light_id, MessageType.SWITCH_ON),
                Message(speaker_id, MessageType.SWITCH_ON),
            ]
        )
        await service.run_sequence(
            [
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG, "Rick Astley - "
                                           "Never Gonna Give You Up"
                )
            ]
        )

    async def sleep_program(
            hue_light_id: str,
            speaker_id: str,
            toilet_id: str
    ) -> None:
        await service.run_parallel(
            [
                Message(speaker_id, MessageType.SWITCH_OFF),
                Message(hue_light_id, MessageType.SWITCH_OFF),
            ]
        )
        await service.run_sequence(
            [
                Message(toilet_id, MessageType.CLEAN),
                Message(toilet_id, MessageType.FLUSH),
            ]
        )

    await wake_up_program(hue_light_id, speaker_id)
    await sleep_program(hue_light_id, speaker_id, toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
