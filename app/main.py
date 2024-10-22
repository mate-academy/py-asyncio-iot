import asyncio
import time
from typing import Any, Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    )

    print("----------------------Start wake up program-----------------------")
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.CHANGE_COLOR)),
            service.send_msg(Message(speaker_id, MessageType.PLAY_SONG,
                                     "Rick Astley - Never Gonna Give You Up")),
        )
    )
    print("----------------------Finish wake up program----------------------")

    # sleep
    print("-----------------------Start sleep program------------------------")
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            run_sequence(
                service.send_msg(Message(toilet_id, MessageType.OPEN)),
                service.send_msg(Message(toilet_id, MessageType.FLUSH))
            )
        ),
        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        service.send_msg(Message(toilet_id, MessageType.CLOSE))
    )
    print("-----------------------Finish sleep program-----------------------")

    await run_parallel(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
