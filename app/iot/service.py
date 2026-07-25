import asyncio
import random
import string
from typing import Any, Awaitable, Protocol

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Async structural subtyping protocol definition
class Device(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(
            self,
            message_type: MessageType,
            data: str = ""
    ) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        # Await connection non-blockingly
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        # Await disconnection non-blockingly
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)


# --- Concurrency Execution Helpers ---
async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Executes coroutines one after another in strict sequential order."""
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    """Executes coroutines simultaneously to save time."""
    await asyncio.gather(*functions)
