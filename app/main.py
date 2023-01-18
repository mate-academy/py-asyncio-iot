import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    devices_id = await asyncio.gather(
        *[
            service.register_device(device)
            for device in [hue_light, speaker, toilet]
        ]
    )

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    await run_parallel(
        service.send_msg(Message(devices_id[0], MessageType.SWITCH_ON)),
        service.send_msg(Message(devices_id[1], MessageType.SWITCH_ON)),
        service.send_msg(Message(devices_id[2], MessageType.OPEN)),
        service.send_msg(
            Message(
                devices_id[1],
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            )
        ),
    )

    await run_sequence(
        run_parallel(
            service.send_msg(Message(devices_id[2], MessageType.FLUSH)),
            service.send_msg(
                Message(
                    devices_id[0],
                    MessageType.CHANGE_COLOR,
                    "Colour change to Green",
                )
            ),
            service.send_msg(Message(devices_id[2], MessageType.CLEAN)),
        ),
        run_sequence(
            service.send_msg(Message(devices_id[0], MessageType.SWITCH_OFF)),
            service.send_msg(Message(devices_id[1], MessageType.SWITCH_OFF)),
            service.send_msg(Message(devices_id[2], MessageType.CLOSE)),
            run_parallel(
                service.unregister_device(devices_id[0]),
                service.unregister_device(devices_id[1]),
                service.unregister_device(devices_id[2]),
            )
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
