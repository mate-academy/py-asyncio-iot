import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_wake_up(service: IOTService, hue_light_id, speaker_id):
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(MEssage(speaker_id, MessageType.SWITCH_ON)),
    )
    await run_sequence(
        service.send_msg(Message(speaker_id, MessageType.PLAY_SONG,  "Rick Astley - Never Gonna Give You Up"))
    )

async def run_sleep(service: IOTService, hue_light_id, speaker_id, toilet_id):
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),

    )
    await run_sequence(
        service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )

async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light, speaker,toilet = HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await service.register_devices([hue_light, speaker, toilet])

    await run_wake_up(service, hue_light_id, speaker_id)
    await run_sleep(service, hue_light_id, speaker_id, toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
