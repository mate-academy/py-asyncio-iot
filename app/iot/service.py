import asyncio
import random
import string
from typing import Protocol

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(
        self, message_type: MessageType, data: str
    ) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        if device_id not in self.devices:
            raise ValueError(f"Device with ID {device_id} not found")
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        if device_id not in self.devices:
            raise ValueError(f"Device with ID {device_id} not found")
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        for msg in program:
            await self.send_msg(msg)
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        if msg.device_id not in self.devices:
            raise ValueError(f"Device with ID {msg.device_id} not found")
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
