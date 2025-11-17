import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from typing import Any, Awaitable


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    results = await asyncio.gather(hue_light_id, speaker_id, toilet_id)

    id_hue_light, id_speaker, id_toilet = results

    parallel_up_program = [
        Message(id_hue_light, MessageType.SWITCH_ON),
        Message(id_speaker, MessageType.SWITCH_ON),
        Message(
            id_toilet, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"
        ),
        Message(id_hue_light, MessageType.SWITCH_OFF),
        Message(id_speaker, MessageType.SWITCH_OFF),
    ]
    parallel_program = [service.send_msg(msg) for msg in parallel_up_program]

    sequence_programs = [
        Message(id_toilet, MessageType.FLUSH),
        Message(id_toilet, MessageType.CLEAN),
    ]
    sequence_program = [service.send_msg(msg) for msg in sequence_programs]

    # run the programs
    async def run_sequence(*sequence_program: Awaitable[Any]) -> None:
        for function in sequence_program:
            await function

    async def run_parallel(*parallel_program: Awaitable[Any]) -> None:
        await asyncio.gather(*parallel_program)


    await run_sequence(*sequence_program)
    await run_parallel(*parallel_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
