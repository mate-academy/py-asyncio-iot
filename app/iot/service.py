import random
import string
from typing import Protocol, Awaitable, Any

import asyncio

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing
# so devices should not inherit for it (if it walks like a duck, and quacks like a duck, it's a duck)
class Device(Protocol):
    async def connect(self) -> None:
        ...  # Ellipsis - similar to "pass", but sometimes has different meaning

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    @staticmethod
    async def run_sequence(*functions: Awaitable[Any]):
        for function in functions:
            await function

    @staticmethod
    async def run_parallel(*functions: Awaitable[Any]):
        await asyncio.gather(*functions)

    @staticmethod
    def create_device_programs(program: list[Message]):
        device_programs = {}
        max_steps = 0
        for msg in program:
            if not msg.device_id in device_programs:
                device_programs[msg.device_id] = []
            device_programs[msg.device_id].append(msg)
            max_steps = max(max_steps, len(device_programs[msg.device_id]))
        return device_programs

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
        device_programs = self.create_device_programs(program)
        await self.run_parallel(*[
            self.run_sequence(*[self.send_msg(msg) for msg in device_program])
            for device_program in device_programs.values()
        ])
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
