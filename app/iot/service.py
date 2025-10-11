import random
import string
import asyncio
from typing import Protocol, Dict

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
        self.devices: Dict[str, Device] = {}

    async def register_devices(self, devices: list[Device]) -> list[str]:
        """Connect and register multiple devices concurrently."""
        # connect all devices at once
        await asyncio.gather(*(device.connect() for device in devices))

        # generate IDs and store them
        ids = []
        for device in devices:
            device_id = generate_id()
            self.devices[device_id] = device
            ids.append(device_id)

        return ids

    async def unregister_all(self) -> None:
        """Disconnect all devices concurrently."""
        await asyncio.gather(*(device.disconnect() for device in self.devices.values()))
        self.devices.clear()

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        """
        WARNING: This method runs all messages concurrently.
        Use only for messages that do NOT require specific ordering.
        For flows that require ordering (e.g., wake-up or sleep flows),
        use explicit run_sequence / run_parallel in main.py.
        """
        print("===== RUNNING PROGRAM =====")
        await asyncio.gather(*(self.send_msg(msg) for msg in program))
        print("===== END OF PROGRAM =====")

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
