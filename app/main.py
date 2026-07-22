import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, Device

from typing import Any, Awaitable


async def register_device(service: IOTService, device: Device) -> dict:
    device_id = await service.register_device(device)
    return {device.NAME: device_id}


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def wake_up(
        service: IOTService,
        hue_light_id: str,
        speaker_id: str
) -> None:
    print("=====RUNNING PROGRAM======")
    await run_parallel(
        service.send_msg(
            Message(hue_light_id, MessageType.SWITCH_ON)
        ),
        run_sequence(
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up"
                )
            ),
        )
    )
    print("=====END OF PROGRAM======")


async def sleep(
        service: IOTService,
        hue_light_id: str,
        speaker_id: str,
        toilet_id: str
) -> None:
    print("=====RUNNING PROGRAM======")
    await run_parallel(
        service.send_msg(
            Message(hue_light_id, MessageType.SWITCH_OFF)
        ),
        service.send_msg(
            Message(speaker_id, MessageType.SWITCH_OFF)
        ),
        run_sequence(
            service.send_msg(
                Message(toilet_id, MessageType.FLUSH)
            ),
            service.send_msg(
                Message(toilet_id, MessageType.CLEAN)
            ),
        )
    )
    print("=====END OF PROGRAM======")


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    devices = []

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    devices.append(hue_light)
    devices.append(speaker)
    devices.append(toilet)

    devices_ids = {}

    register_devices = await asyncio.gather(
        *(register_device(service, device) for device in devices)
    )

    for registered_device in register_devices:
        devices_ids.update(registered_device)

    hue_light_id = devices_ids[hue_light.NAME]
    speaker_id = devices_ids[speaker.NAME]
    toilet_id = devices_ids[toilet.NAME]

    # create a few programs
    # wake_up_program = [
    #     Message(hue_light_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.SWITCH_ON),
    #     Message(
    #     speaker_id,
    #     MessageType.PLAY_SONG,
    #     "Rick Astley - Never Gonna Give You Up"
    #     ),
    # ]
    #
    # sleep_program = [
    #     Message(hue_light_id, MessageType.SWITCH_OFF),
    #     Message(speaker_id, MessageType.SWITCH_OFF),
    #     Message(toilet_id, MessageType.FLUSH),
    #     Message(toilet_id, MessageType.CLEAN),
    # ]
    #
    # # run the programs
    # await service.run_program(wake_up_program)
    # await service.run_program(sleep_program)

    await wake_up(service, hue_light_id, speaker_id)
    await sleep(service, hue_light_id, speaker_id, toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
