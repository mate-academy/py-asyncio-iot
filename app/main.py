import time
import asyncio

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType


async def run_commands_sequence(*commands) -> None:
    for command in commands:
        await command


async def run_commands_parallel(*commands) -> None:
    await asyncio.gather(*commands)


async def main() -> None:

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    await run_commands_parallel(
        hue_light.send_message(MessageType.SWITCH_ON),
        speaker.send_message(MessageType.SWITCH_ON)
    )

    await run_commands_sequence(
        speaker.send_message(
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    )

    await run_commands_parallel(
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF)
    )

    await run_commands_sequence(
        toilet.send_message(MessageType.FLUSH),
        toilet.send_message(MessageType.CLEAN)
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
