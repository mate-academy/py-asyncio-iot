import asyncio
import random
import string
from typing import Any, Awaitable, Protocol

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    """Generate random device ID using uppercase ASCII letters."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    """Protocol defining required methods for IoT devices."""

    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class DeviceRegistry:
    """Registry for managing IoT devices."""

    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register(self, device: Device) -> str:
        """Connect and register new device, return device ID."""
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister(self, device_id: str) -> None:
        """Disconnect and remove device from service."""
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        """Retrieve device instance by ID."""
        return self.devices[device_id]


class MessageHandler:
    """Handler for processing device messages."""

    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    async def send_message(self, msg: Message) -> None:
        """Send message to specified device."""
        device = self.registry.get_device(msg.device_id)
        await device.send_message(msg.msg_type, msg.data)

    async def run_program(self, program: list[Message]) -> None:
        """Execute sequence of IoT device messages."""
        print("=====RUNNING PROGRAM======")
        for msg in program:
            await self.send_message(msg)
        print("=====END OF PROGRAM======")


class IOTService:
    """Service for managing IoT devices and message handling."""

    def __init__(self) -> None:
        self.registry = DeviceRegistry()
        self.message_handler = MessageHandler(self.registry)

    async def register_device(self, device: Device) -> str:
        """Register new device."""
        return await self.registry.register(device)

    async def unregister_device(self, device_id: str) -> None:
        """Unregister device."""
        await self.registry.unregister(device_id)

    def get_device(self, device_id: str) -> Device:
        """Get device by ID."""
        return self.registry.get_device(device_id)

    async def send_msg(self, msg: Message) -> None:
        """Send message to device."""
        await self.message_handler.send_message(msg)

    async def run_program(self, program: list[Message]) -> None:
        """Run program of messages."""
        await self.message_handler.run_program(program)


async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Execute given async functions in sequence."""
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> tuple:
    """Execute given async functions in parallel."""
    return await asyncio.gather(*functions)
