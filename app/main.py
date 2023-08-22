import time
import asyncio
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

    # hue_light = service.register_device(HueLightDevice())
    # speaker = service.register_device(SmartSpeakerDevice())
    # toilet = service.register_device(SmartToiletDevice())

    # hue_light_id = service.register_device(hue_light)
    # speaker_id = service.register_device(speaker)
    # toilet_id = service.register_device(toilet)

    # devices_for_register = [hue_light, speaker, toilet]
    # devices = await asyncio.gather(*devices_for_register)
    # print(type(devices))
    # print(devices)
    # hue_light_id, speaker_id, toilet_id = devices

    # hue_light_id = (await asyncio.gather(service.register_device(HueLightDevice())))[0]
    # speaker_id = (await asyncio.gather(service.register_device(SmartSpeakerDevice())))[0]
    # toilet_id = (await asyncio.gather(service.register_device(SmartToiletDevice())))[0]

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        *[
            service.register_device(HueLightDevice()),
            service.register_device(SmartSpeakerDevice()),
            service.register_device(SmartToiletDevice())
        ]
    )

    # create a few programs
    # wake_up_program = [
    #     Message(hue_light_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    # ]
    #
    # sleep_program = [
    #     Message(toilet_id, MessageType.FLUSH),
    #     Message(toilet_id, MessageType.CLEAN),
    #     Message(hue_light_id, MessageType.SWITCH_OFF),
    #     Message(speaker_id, MessageType.SWITCH_OFF),
    # ]

    # run the programs
    # await service.run_program(wake_up_program)
    # await service.run_program(sleep_program)

    #========================================================================

    parallel_wake_up_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
    ]
    sequence_wake_up_program = [
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"
            )
        )
    ]

    sequence_sleep_program = [
        service.send_msg(Message(toilet_id, MessageType.CLEAN))
    ]

    parallel_sleep_program = [
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(toilet_id, MessageType.FLUSH))
    ]

    await run_parallel(*parallel_wake_up_program)
    await run_sequence(*sequence_wake_up_program)

    await run_sequence(*sequence_sleep_program)
    await run_parallel(*parallel_sleep_program)

    #=======================================================

    # await run_sequence(
    #     run_parallel(
    #         service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
    #         service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
    #     ),
    #     service.send_msg(
    #         Message(
    #             speaker_id,
    #             MessageType.PLAY_SONG,
    #             "Rick Astley - Never Gonna Give You Up"
    #         )
    #     )
    # )
    #
    # await run_sequence(
    #     run_parallel(
    #         service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
    #         service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
    #         service.send_msg(Message(toilet_id, MessageType.FLUSH))
    #     ),
    #     service.send_msg(Message(toilet_id, MessageType.CLEAN))
    # )
    #==============================================================================

    await run_sequence()

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
