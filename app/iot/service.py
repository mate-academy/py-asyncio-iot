import asyncio
import random
import string
from typing import Protocol, Any, Awaitable

from .message import MessageType, Message


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


async def run_sequence(*functions: Awaitable[Any]) -> None:
    """
    Run awaitables one after another in the given order.

    Args:
        *functions: Awaitable objects (already called coroutines).
                    Pass awaitable objects (already-called coroutines),
                    e.g. pass func() not func
    """
    for func in functions:
        await func


async def run_parallel(*functions: Awaitable[Any]) -> None:
    """
    Run awaitables concurrently (fire-and-wait semantics).

    Args:
        *functions: Awaitable objects (already called coroutines).
                    Pass awaitable objects (already-called coroutines), e.g. pass func() not func
    """
    await asyncio.gather(*functions)


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def register_devices(self, devices: list[Device]) -> list[str]:
        return list(
            await asyncio.gather(
                *(self.register_device(device) for device in devices)
            )
        )

    async def unregister_device(self, device_id: str) -> None:
        if device_id not in self.devices:
            raise ValueError(f"Device {device_id} not found")
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        if device_id not in self.devices:
            raise ValueError(f"Device {device_id} not found")
        return self.devices[device_id]

    async def send_message(self, msg: Message) -> None:
        """Send a single message to a registered device."""
        if msg.device_id not in self.devices:
            raise ValueError(f"Device {msg.device_id} not found")
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)

    async def run_program(self, program: list[Message]) -> None:
        """
        Run a list of messages sequentially (legacy mode).
        Consider replacing with run_sequence / run_parallel in new code.
        """
        print("=====RUNNING PROGRAM======")
        for msg in program:
            await self.send_message(msg)
        print("=====END OF PROGRAM======")
