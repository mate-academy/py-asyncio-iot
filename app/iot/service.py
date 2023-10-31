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

    def unregister_device(self, device_id: str) -> None:
        self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_sequence(self, program: list[Message]) -> None:
        print("=====RUNNING SEQUENCE PROGRAM======")
        for msg in program:
            await self.send_msg(msg)
        print("=====END OF SEQUENCE PROGRAM======")

    async def run_parallel(self, programs: list[list]) -> None:
        print("=====RUNNING PARALLEL PROGRAM======")
        tasks = []
        for program in programs:
            tasks.append(self.run_sequence(program))
        await asyncio.gather(*tasks)
        print("=====END OF PARALLEL PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
