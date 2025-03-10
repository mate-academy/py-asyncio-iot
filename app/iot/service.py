import asyncio
import random
import string
from typing import Any, Awaitable, Protocol
from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def send_message(self,
                           message_type:
                           MessageType, data: str) -> None:
        pass


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
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)

    async def run_sequence(self, *functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(self, *functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    async def run_wake_up_program(self,
                                  hue_light_id:
                                  str, speaker_id: str) -> None:
        await self.run_parallel(
            self.send_msg(Message(hue_light_id, MessageType.SWITCH_ON)),
            self.send_msg(Message(speaker_id, MessageType.SWITCH_ON)),
        )
        await self.send_msg(Message(speaker_id,
                                    MessageType.PLAY_SONG,
                                    "Rick Astley - Never Gonna Give You Up"))

    async def run_sleep_program(self,
                                hue_light_id: str,
                                speaker_id: str,
                                toilet_id: str) -> None:
        await self.run_parallel(
            self.send_msg(Message(hue_light_id, MessageType.SWITCH_OFF)),
            self.send_msg(Message(speaker_id, MessageType.SWITCH_OFF)),
        )
        await self.run_sequence(
            self.send_msg(Message(toilet_id, MessageType.FLUSH)),
            self.send_msg(Message(toilet_id, MessageType.CLEAN)),
        )
