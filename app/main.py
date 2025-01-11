import time
import asyncio
from typing import List
from enum import Enum


class MessageType(Enum):
    SWITCH_ON = "SWITCH_ON"
    SWITCH_OFF = "SWITCH_OFF"
    PLAY_SONG = "PLAY_SONG"
    FLUSH = "FLUSH"
    CLEAN = "CLEAN"


class Message:
    def __init__(self, device_id: str,
                 msg_type: str,
                 content: str = None) -> None:
        self.device_id = device_id
        self.type = msg_type
        self.content = content


class IOTService:
    def __init__(self) -> None:
        self.devices = {}

    async def register_device(self, device: str) -> str:
        """Asynchronously register a device."""
        device_id = str(len(self.devices) + 1)
        self.devices[device_id] = device
        print(f"Device {device.__class__.__name__} "
              f"registered with ID {device_id}")
        return device_id

    async def send_message(self, message: Message) -> None:
        """Asynchronously send a message to a device."""
        print(f"Sending message to device "
              f"{message.device_id}: {message.type}")
        await asyncio.sleep(1)
        print(f"Message sent: "
              f"{message.device_id} - {message.type}")


async def run_sequence(*functions) -> None:
    """Run functions in sequence (one after the other)."""
    for function in functions:
        await function


async def run_parallel(*functions) -> None:
    """Run functions in parallel."""
    await asyncio.gather(*functions)


async def async_run_program(
        service: IOTService,
        program: List[Message]
) -> None:
    """Run the program asynchronously."""
    tasks = [service.send_message(message)
             for message in program]
    await asyncio.gather(*tasks)


async def main() -> None:
    service = IOTService()

    class HueLightDevice:
        pass

    class SmartSpeakerDevice:
        pass

    class SmartToiletDevice:
        pass

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    device_ids = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    hue_light_id, speaker_id, toilet_id = device_ids

    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    await run_parallel(
        service.send_message(wake_up_program[0]),
        service.send_message(wake_up_program[1]),
        service.send_message(wake_up_program[2])
    )

    await run_sequence(
        service.send_message(sleep_program[0]),
        service.send_message(sleep_program[1]),
        service.send_message(sleep_program[2]),
        service.send_message(sleep_program[3])
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
