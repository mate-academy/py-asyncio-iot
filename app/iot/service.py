import asyncio

import random
import string
from typing import Protocol, Any, Awaitable

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


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

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        tasks = []
        for msg in program:
            tasks.append(self.send_msg(msg))
        await asyncio.gather(*tasks)
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        device = self.devices[msg.device_id]
        await device.send_message(msg.msg_type, msg.data)

    async def register_devices_simultaneously(
            self,
            devices: list[Device]
    ) -> list[str]:

        tasks = [self.register_device(device) for device in devices]
        device_ids = await asyncio.gather(*tasks)
        return device_ids
