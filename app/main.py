import asyncio
import time
from typing import Awaitable, Any

from app.iot.devices  import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from app.iot.message import Message, MessageType
from app.iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def wake_up(
    service: IOTService,
    light_id: str,
    speaker_id: str,
) -> None:
    print("===== WAKE UP PROGRAM =====")

    await run_sequence(
        run_parallel(
            service.send_msg(
                Message(light_id, MessageType.SWITCH_ON)
            ),
            service.send_msg(
                Message(speaker_id, MessageType.SWITCH_ON)
            ),
        ),
        service.send_msg(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Morning playlist",
            )
        ),
    )

    print("===== END WAKE UP =====")


async def sleep(
    service: IOTService,
    light_id: str,
    speaker_id: str,
    toilet_id: str,
) -> None:
    print("===== SLEEP PROGRAM =====")

    await run_parallel(
        service.send_msg(
            Message(light_id, MessageType.SWITCH_OFF)
        ),
        service.send_msg(
            Message(speaker_id, MessageType.SWITCH_OFF)
        ),
        run_sequence(
            service.send_msg(
                Message(toilet_id, MessageType.FLUSH)
            ),
            service.send_msg(
                Message(toilet_id, MessageType.CLEAN)
            ),
        ),
    )

    print("===== END SLEEP =====")


async def main() -> None:
    service = IOTService()

    light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    await wake_up(service, light_id, speaker_id)

    await asyncio.sleep(1)

    await sleep(service, light_id, speaker_id, toilet_id)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
