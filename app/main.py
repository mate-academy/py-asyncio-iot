import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService

async def connect(service, device):
    return await asyncio.to_thread(service.register_device, device)

async def disconnect(service, device_id):
    return await asyncio.to_thread(service.unregister_device, device_id)

async def send_message(service, message):
    return await asyncio.to_thread(service.send_msg, message)

async def run_sequence(*functions):
    for function in functions:
        await function

async def run_parallel(*functions):
    await asyncio.gather(*functions)

async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        connect(service, hue_light),
        connect(service, speaker),
        connect(service, toilet)
    )

    # create a few programs
    await run_parallel(
        send_message(service, Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            send_message(service, Message(speaker_id, MessageType.SWITCH_ON)),
            send_message(service, Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
        )
    )

    await run_parallel(
        send_message(service, Message(hue_light_id, MessageType.SWITCH_OFF)),
        send_message(service, Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            send_message(service, Message(toilet_id, MessageType.FLUSH)),
            send_message(service, Message(toilet_id, MessageType.CLEAN))
        )
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
