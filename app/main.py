import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions) -> None:
    for func in functions:
        await func


async def run_parallel(*functions) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    device_ids = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )
    hue_light_id, speaker_id, toilet_id = device_ids

    async def wake_up() -> None:
        await run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            run_sequence(
                service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
                service.send_msg(
                    Message(
                        speaker_id,
                        MessageType.PLAY_SONG,
                        "Rick Astley - Never Gonna Give You Up"
                    )
                )
            ),
        )

    async def sleep() -> None:
        await run_parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            run_sequence(
                service.send_msg(Message(toilet_id, MessageType.FLUSH)),
                service.send_msg(Message(toilet_id, MessageType.CLEAN))
            ),
        )

    print("=====RUNNING WAKE UP PROGRAM======")
    await wake_up()
    print("=====END OF WAKE UP PROGRAM======\n")

    print("=====RUNNING SLEEP PROGRAM======")
    await sleep()
    print("=====END OF SLEEP PROGRAM======\n")

    await asyncio.gather(
        service.unregister_device(hue_light_id),
        service.unregister_device(speaker_id),
        service.unregister_device(toilet_id),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
