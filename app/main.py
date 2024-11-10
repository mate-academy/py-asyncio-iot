import time
import asyncio
from typing import Awaitable, Any


from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType

# from iot.service import IOTService


# Function to run tasks concurrently
async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


# Function to run tasks sequentially
async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def main() -> None:
    # create an IOT service
    # service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    # hue_light_id = service.register_device(hue_light)
    # speaker_id = service.register_device(speaker)
    # toilet_id = service.register_device(toilet)

    # connect devices concurrently
    # await asyncio.gather(
    #     hue_light.connect(),
    #     speaker.connect(),
    #     toilet.connect(),
    # )

    # create a few programs
    # wake_up_program = [
    #     Message(hue_light_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.SWITCH_ON),
    #     Message(
    #         speaker_id,
    #         MessageType.PLAY_SONG,
    #         "Rick Astley - Never Gonna Give You Up",
    #     ),
    # ]

    # sleep_program = [
    #     Message(hue_light_id, MessageType.SWITCH_OFF),
    #     Message(speaker_id, MessageType.SWITCH_OFF),
    #     Message(toilet_id, MessageType.FLUSH),
    #     Message(toilet_id, MessageType.CLEAN),
    # ]

    # run the programs
    # service.run_program(wake_up_program)
    # service.run_program(sleep_program)

    # Wake-up program actions
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_ON),
        speaker.send_message(MessageType.SWITCH_ON),
    )

    # Sequentially play the song on the speaker
    await run_sequence(
        speaker.send_message(
            MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
    )

    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF),
    )

    # Sequentially flush and clean the toilet
    await run_sequence(
        toilet.send_message(MessageType.FLUSH),
        toilet.send_message(MessageType.CLEAN),
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
