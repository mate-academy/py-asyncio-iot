import asyncio
import random
import string
from typing import Protocol, Any, Awaitable

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing
class Device(Protocol):
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def send_message(self, message_type: MessageType, data: str) -> None: ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        """Connects the device and registers it with a unique ID"""
        await device.connect()
        while True:
            device_id = generate_id()
            if device_id not in self.devices:
                break
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        """Disables the device and removes it from the registry."""
        if device_id not in self.devices:
            raise ValueError(f"Unknown device id: {device_id}")
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        if device_id not in self.devices:
            raise ValueError(f"Unknown device id: {device_id}")
        return self.devices[device_id]

    async def send_msg(self, msg: Message) -> None:
        """Sends a message to a registered device."""
        if msg.device_id not in self.devices:
            raise ValueError(f"Unknown device id: {msg.device_id}")
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)


async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Runs awaitables in strict sequence, one after the other."""
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    """Runs awaitable in parallel.
    Exceptions from any task propagate outwards via asyncio.gather.
    """
    await asyncio.gather(*functions)
