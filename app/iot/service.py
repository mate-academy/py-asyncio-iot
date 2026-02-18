import asyncio
import random
import string
from typing import Any, Awaitable, Protocol

from .message import Message, MessageType


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing
# so devices should not inherit for it (if it walks like a duck,
# and quacks like a duck, it's a duck)
class Device(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(
            self,
            message_type: MessageType,
            data: str
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
            raise ValueError("Invalid device_id")
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        if device_id not in self.devices:
            raise ValueError("Invalid device_id")
        return self.devices[device_id]

    async def run_program(
            self,
            program: list[Message],
            *,
            in_parallel: bool = False
    ) -> None:
        print("=====RUNNING PROGRAM======")

        awaitables = [self.send_msg(msg) for msg in program]

        if in_parallel:
            await run_parallel(*awaitables)
        else:
            await run_sequence(*awaitables)

        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        if msg.device_id not in self.devices:
            raise ValueError("Invalid device_id")
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
