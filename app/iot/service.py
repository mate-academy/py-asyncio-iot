import random
import string
from typing import Protocol, Optional

from app.iot.message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    async def send_message(
        self, message_type: MessageType, data: Optional[str] = None
    ) -> None: ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        print(f"Device {device_id} registered.")
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        if device_id in self.devices:
            await self.devices[device_id].disconnect()
            del self.devices[device_id]
            print(f"Device {device_id} unregistered.")
        else:
            print(f"Device {device_id} not found.")

    def get_device(self, device_id: str) -> Optional[Device]:
        return self.devices.get(device_id)

    async def send_message(self, msg: Message) -> None:
        device = self.devices.get(msg.device_id)
        if device:
            await device.send_message(msg.msg_type, msg.data)
        else:
            print(f"Device with ID {msg.device_id} not found.")

    async def run_program(self, program: list[Message]) -> None:
        print("===== RUNNING PROGRAM =====")
        for msg in program:
            await self.send_message(msg)
        print("===== END OF PROGRAM =====")
