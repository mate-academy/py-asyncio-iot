import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


def speaker_actions(service: IOTService, speaker_id: str):
    async def actions():
        await run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(
                Message(
                    speaker_id,
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up",
                )
            ),
        )

    return actions


def toilet_actions(service: IOTService, toilet_id: str):
    async def actions():
        await run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )

    return actions


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def registration() -> tuple[IOTService, str, str, str]:
    service = IOTService()
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )
    return service, hue_light_id, speaker_id, toilet_id


async def run() -> None:
    service, hue_light_id, speaker_id, toilet_id = await registration()

    speaker_actions_function = speaker_actions(service, speaker_id)
    await service.run_program(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        speaker_actions_function(),
    )

    toilet_actions_function = toilet_actions(service, toilet_id)
    await service.run_program(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        toilet_actions_function(),
    )


def main() -> None:
    start = time.perf_counter()
    asyncio.run(run())
    end = time.perf_counter()
    print("Elapsed:", end - start)


if __name__ == "__main__":
    main()
