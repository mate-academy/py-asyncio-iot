import random
import string
import asyncio
from typing import Protocol, Any, Awaitable

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(
            msg.msg_type,
            msg.data,
        )


    async def wake_up(self, hue_light_id: str, speaker_id: str, toilet_id: str) -> None:
        print("===== RUNNING WAKE UP PROGRAM =====")

        await run_parallel(
            self.devices[hue_light_id].send_message(
                MessageType.SWITCH_ON, ""
            ),
            run_sequence(
                self.devices[speaker_id].send_message(
                    MessageType.SWITCH_ON, ""
                ),
                self.devices[speaker_id].send_message(
                    MessageType.PLAY_SONG,
                    "Rick Astley - Never Gonna Give You Up",
                ),
            ),
            run_sequence(
                self.devices[toilet_id].send_message(
                    MessageType.FLUSH, ""
                ),
                self.devices[toilet_id].send_message(
                    MessageType.CLEAN, ""
                ),
            ),
        )

        print("===== END OF WAKE UP PROGRAM =====")

    async def sleep(self, hue_light_id: str, speaker_id: str, toilet_id: str) -> None:
        print("===== RUNNING SLEEP PROGRAM =====")

        await run_parallel(
            self.devices[hue_light_id].send_message(
                MessageType.SWITCH_OFF, ""
            ),
            self.devices[speaker_id].send_message(
                MessageType.SWITCH_OFF, ""
            ),
            run_sequence(
                self.devices[toilet_id].send_message(
                    MessageType.CLEAN, ""
                ),
                self.devices[toilet_id].send_message(
                    MessageType.FLUSH, ""
                ),
            ),
        )

        print("===== END OF SLEEP PROGRAM =====")
