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
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

# why this variant not working? (question to QnA)
    # hue_light_id = asyncio.create_task(service.register_device(hue_light))
    # speaker_id = asyncio.create_task(service.register_device(speaker))
    # toilet_id = asyncio.create_task(service.register_device(toilet))
    #
    # await asyncio.gather(hue_light_id, speaker_id, toilet_id)

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # run the programs
    await run_sequence(
        # wake up program
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON))
        ),
        service.send_msg(Message(
            speaker_id, MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up")
        ),
        # sleep program
        run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(toilet_id, MessageType.FLUSH))
        ),
        service.send_msg(Message(toilet_id, MessageType.CLEAN))
    )

# old version
    # create a few programs
    # wake_up_program = [
    #     Message(hue_light_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
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
    # service.run_program(wake_up_program)
    # service.run_program(sleep_program)



if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
