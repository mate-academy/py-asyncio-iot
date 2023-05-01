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
    service = IOTService()

    device_id_list = await asyncio.gather(
        *[service.register_device(device)
          for device in
          (HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice())]
    )

    wake_up_program = [
        Message(device_id_list[0], MessageType.SWITCH_ON),
        Message(device_id_list[1], MessageType.SWITCH_ON),
        Message(
            device_id_list[1],
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sleep_program = [
        Message(device_id_list[0], MessageType.SWITCH_OFF),
        Message(device_id_list[1], MessageType.SWITCH_OFF),
        Message(device_id_list[2], MessageType.FLUSH),
        Message(device_id_list[2], MessageType.CLEAN),
    ]

    await run_sequence(
        run_parallel(
            service.send_msg(wake_up_program[0]),
            service.send_msg(wake_up_program[1])
        ),
        service.send_msg(wake_up_program[2]),

        run_parallel(
            service.send_msg(sleep_program[0]),
            service.send_msg(sleep_program[1]),
            service.send_msg(sleep_program[2])
        ),
        service.send_msg(sleep_program[2]),

        run_parallel(
            *[service.unregister_device(device_id)
              for device_id in device_id_list]
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
