import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_concurrently(*functions: asyncio.coroutines) -> None:
    await asyncio.gather(*functions)


async def main() -> None:
    service = IOTService()

    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice()]

    device_tasks = await asyncio.gather(
        *[service.register_device(device) for device in devices]
    )
    device_ids = dict(
        zip([type(device).__name__ for device in devices], device_tasks)
    )

    await run_concurrently(
        service.send_msg(
            Message(device_ids["HueLightDevice"], MessageType.SWITCH_ON)
        ),
        service.send_msg(
            Message(device_ids["SmartSpeakerDevice"], MessageType.SWITCH_ON)
        ),
    )

    await asyncio.sleep(0.1)

    await run_concurrently(
        service.send_msg(
            Message(
                device_ids["SmartSpeakerDevice"],
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            )
        ),
    )

    await run_concurrently(
        service.send_msg(
            Message(device_ids["HueLightDevice"], MessageType.SWITCH_OFF)
        ),
        service.send_msg(
            Message(device_ids["SmartSpeakerDevice"], MessageType.SWITCH_OFF)
        ),
        service.send_msg(
            Message(device_ids["SmartToiletDevice"], MessageType.FLUSH)
        ),
    )
    await asyncio.sleep(0.1)

    await run_concurrently(
        service.send_msg(
            Message(device_ids["SmartToiletDevice"], MessageType.CLEAN)
        ),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed time:", end - start)
