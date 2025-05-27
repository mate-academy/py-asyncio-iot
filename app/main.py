import asyncio
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*funtions: Awaitable[Any]) -> None:
    for funtion in funtions:
        await funtion


async def run_parallel(*funtions: Awaitable[Any]) -> None:
    await asyncio.gather(*funtions)


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
    await service.run_program(
        run_sequence(
            run_parallel(
                service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
                service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            ),
            service.send_msg(Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            ))
        )
    )

    await service.run_program(
         run_sequence(
            run_parallel(
                service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
                service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            ),
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    )


if __name__ == "__main__":
    import time
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
