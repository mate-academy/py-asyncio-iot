import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()
    devices_ids = {}

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    registered_devices = await asyncio.gather(
        *[service.register_device(device) for device in (hue_light, speaker, toilet,)]
    )
    for device_id in registered_devices:
        device = service.get_device(device_id)
        variable_name = device.variable_name()
        devices_ids[f"{variable_name}_id"] = device_id

    # create a few programs
    wake_up_program = [
        Message(devices_ids["hue_light_id"], MessageType.SWITCH_ON),
        Message(devices_ids["speaker_id"], MessageType.SWITCH_ON),
        Message(devices_ids["speaker_id"], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(devices_ids["hue_light_id"], MessageType.SWITCH_OFF),
        Message(devices_ids["speaker_id"], MessageType.SWITCH_OFF),
        Message(devices_ids["toilet_id"], MessageType.FLUSH),
        Message(devices_ids["toilet_id"], MessageType.CLEAN),
    ]

    # run the programs
    for program in [wake_up_program, sleep_program]:
        await service.run_program(program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
