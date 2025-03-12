import asyncio
import time
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_sequence, run_parallel


async def main() -> None:
    service = IOTService()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(HueLightDevice()),
        service.register_device(SmartSpeakerDevice()),
        service.register_device(SmartToiletDevice()),
    )

    programs = {
        "wake_up": [
            {
                "mode": "parallel",
                "msgs": [
                    Message(hue_light_id, MessageType.SWITCH_ON),
                    Message(speaker_id, MessageType.SWITCH_ON),
                ],
            },
            {
                "mode": "sequence",
                "msgs": [
                    Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
                ],
            },
        ],
        "sleep": [
            {
                "mode": "parallel",
                "msgs": [
                    Message(hue_light_id, MessageType.SWITCH_OFF),
                    Message(speaker_id, MessageType.SWITCH_OFF),
                ],
            },
            {
                "mode": "sequence",
                "msgs": [
                    Message(toilet_id, MessageType.FLUSH),
                    Message(toilet_id, MessageType.CLEAN),
                ],
            },
        ],
    }

    async def run_program(program):
        for group in program:
            if group["mode"] == "parallel":
                await run_parallel(*(service.send_msg(msg) for msg in group["msgs"]))
            elif group["mode"] == "sequence":
                await run_sequence(*(service.send_msg(msg) for msg in group["msgs"]))

    await run_program(programs["wake_up"])
    await run_program(programs["sleep"])


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("Elapsed:", end - start)
