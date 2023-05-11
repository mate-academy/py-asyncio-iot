import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # # create an IOT service
    service = IOTService()

    devices = (HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice())
    device_ids = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )

    hue_light_id, speaker_id, toilet_id = device_ids

    async def run_program(*funcs) -> None:
        for func in funcs:
            await func

    async def parallel(*funcs) -> None:
        await asyncio.gather(*funcs)

    await run_program(
        parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        ),

        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            )
        ),

        parallel(
            service.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
            service.send_msg(Message(toilet_id, MessageType.FLUSH)),
        ),

        service.send_msg(Message(toilet_id, MessageType.CLEAN)),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
