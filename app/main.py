import asyncio

from iot.devices import (
    HueLightDevice,
    SmartSpeakerDevice,
    SmartToiletDevice
)
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*coroutines: asyncio.coroutines) -> None:
    for coroutine in coroutines:
        await coroutine


async def run_parallel(*coroutines: asyncio.coroutines) -> None:
    await asyncio.gather(*coroutines)


async def main() -> None:
    service = IOTService()

    # створюємо пристрої
    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()]
    # паралельна реєстрація
    device_ids = await service.register_multiple_devices(devices)
    hue_light_id, speaker_id, toilet_id = device_ids

    # === WAKE UP PROGRAM ===
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.PLAY_SONG,
                                     "Rick Astley - Never Gonna Give You Up"))
        )
    )

    # === SLEEP PROGRAM ===
    await run_parallel(
        service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN))
        )
    )


if __name__ == "__main__":
    import time
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
