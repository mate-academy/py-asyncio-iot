import asyncio
from typing import Any, Awaitable

from iot.service import IOTService
from iot.message import Message, MessageType
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    light = HueLightDevice()

    speaker_id, toilet_id, light_id = await asyncio.gather(
        service.register_device(speaker),
        service.register_device(toilet),
        service.register_device(light)
    )

    print("--- Устройства зарегистрированы, запускаем Wake Up ---")

    await run_parallel(
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON, "")),
            service.send_msg(
                Message(speaker_id, MessageType.PLAY_SONG, "Miles Davis")
            )
        ),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH, "")),
            service.send_msg(Message(toilet_id, MessageType.CLEAN, ""))
        ),
        service.send_msg(Message(light_id, MessageType.SWITCH_ON, ""))
    )

    print("--- Запускаем Sleep ---")

    await run_parallel(
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF, ""))
        ),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH, "")),
            service.send_msg(Message(toilet_id, MessageType.CLEAN, ""))
        ),
        service.send_msg(Message(light_id, MessageType.SWITCH_OFF, ""))
    )

    await run_parallel(
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
        service.unregister_device(light_id)
    )


if __name__ == "__main__":
    asyncio.run(main())
