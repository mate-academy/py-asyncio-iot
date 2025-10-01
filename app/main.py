import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)


async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

async def main() -> None:

    service = IOTService()
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    device_list = [hue_light, speaker, toilet]
    results = await asyncio.gather(*(service.register_device(device) for device in device_list))
    await run_sequence(
        run_parallel(
            service.send_msg(Message(results[0], MessageType.SWITCH_ON)),
            service.send_msg(Message(results[1], MessageType.SWITCH_ON))
        ),
        service.send_msg(Message(results[1], MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"))
    )

    await run_sequence(
          run_parallel(
                service.send_msg(Message(results[0], MessageType.SWITCH_OFF)),
                service.send_msg(Message(results[1], MessageType.SWITCH_OFF)),
                service.send_msg(Message(results[2], MessageType.FLUSH))
          ),
          service.send_msg(Message(results[2], MessageType.CLEAN))
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
