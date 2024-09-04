import asyncio
import time
from typing import Any, Awaitable


from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    print("=====RUNNING PROGRAM SEQUENCE======")
    for function in functions:
        await function
    print("=====END OF PROGRAM SEQUENCE======")


async def run_parallel(*functions: Awaitable[Any]) -> None:
    print("=====RUNNING PROGRAM PARALLEL======")
    await asyncio.gather(*functions)
    print("=====END OF PROGRAM PARALLEL======")


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
    # wake up programms
    await run_parallel(
        service.send_msg(
            Message(hue_light_id, MessageType.SWITCH_ON),
        ),
        run_sequence(
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_ON),
            ),
            service.run_program(
                [
                    Message(
                        speaker_id,
                        MessageType.PLAY_SONG,
                        "Rick Astley - Never Gonna Give You Up",
                    ),
                ]
            ),
        ),
    )

    # sleep programms
    await run_parallel(
        run_sequence(
            service.send_msg(
                Message(toilet_id, MessageType.FLUSH),
            ),
            service.send_msg(
                Message(toilet_id, MessageType.CLEAN),
            ),
        ),
        service.send_msg(
            Message(hue_light_id, MessageType.SWITCH_OFF),
        ),
        service.send_msg(
            Message(speaker_id, MessageType.SWITCH_OFF),
        ),
    )

    # unregistering
    hue_light_unregistering = service.unregister_device(hue_light_id)
    speaker_unregistering = service.unregister_device(speaker_id)
    toilet_id_unregistering = service.unregister_device(toilet_id)

    await asyncio.gather(
        hue_light_unregistering, speaker_unregistering, toilet_id_unregistering
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
