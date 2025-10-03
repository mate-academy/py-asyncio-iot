import asyncio
import random
import string
from typing import Protocol, Awaitable

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

    async def register_devices(self, devices: list[Device]) -> list[str]:
        return await asyncio.gather(*(self.register_device(d) for d in devices))

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        if device_id in self.devices:
            await self.devices[device_id].disconnect()
            del self.devices[device_id]
        else:
            print(f"Warning: Device ID {device_id} not found for unregistration.")

    def send_msg(self, msg: Message) -> Awaitable[None]:
        if msg.device_id in self.devices:
            device = self.devices[msg.device_id]
            return device.send_message(msg.msg_type, msg.data)
        else:
            async def no_op():
                print(
                    f"KeyError: Device not found, missing device_id"
                )
            return no_op()
