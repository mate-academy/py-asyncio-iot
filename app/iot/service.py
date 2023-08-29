import asyncio
import random
import string
from typing import Protocol, List
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

    async def run_program(self, program: List[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        await asyncio.gather(*[self.send_message(msg) for msg in program])
        print("=====END OF PROGRAM======")

    async def send_message(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
