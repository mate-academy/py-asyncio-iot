import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*coros):
    for coro in coros:
        await coro

async def run_parallel(*coros):
    await asyncio.gather(*coros)


async def main() -> None:
    service = IOTService()

    # Register devices concurrently
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    async with asyncio.TaskGroup() as tg:
        hue_task = tg.create_task(service.register_device(hue_light))
        speaker_task = tg.create_task(service.register_device(speaker))
        toilet_task = tg.create_task(service.register_device(toilet))

    hue_id = hue_task.result()
    speaker_id = speaker_task.result()
    toilet_id = toilet_task.result()

    # Wake up program: light and speaker ON -> THEN play music
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),
        service.send_msg(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
    )

    # Sleep program: light and speaker OFF, then toilet flush -> clean
    await run_sequence(
        run_parallel(
            service.send_msg(Message(hue_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
        run_sequence(
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
            service.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
