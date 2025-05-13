import asyncio
import random
import string
from typing import Protocol, runtime_checkable
from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing
@runtime_checkable
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
        """Register a device, connect it, and return its ID."""
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        """Unregister a device and disconnect it."""
        device = self.devices.get(device_id)
        if device:
            await device.disconnect()
            del self.devices[device_id]
        else:
            print(f"Device with ID {device_id} not found.")

    def get_device(self, device_id: str) -> Device:
        """Retrieve a device by its ID."""
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        """Run a sequence of messages as a program."""
        print("=====RUNNING PROGRAM======")
        for msg in program:
            await self.send_msg(msg)
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        """Send a message to a device."""
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)

    async def run_sequence(self, *tasks: asyncio.Future) -> None:
        """Run tasks in sequence."""
        for task in tasks:
            await task

    async def run_parallel(self, *tasks: asyncio.Future) -> None:
        """Run tasks in parallel."""
        await asyncio.gather(*tasks)
