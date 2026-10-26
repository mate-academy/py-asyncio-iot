import string
import random
from typing import Dict, Any

from iot.message import Message


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


class IOTService:
    def __init__(self) -> None:
        self.devices: Dict[str, Any] = {}

    async def register_device(self, device: Any) -> str:
        device_id = generate_id()
        self.devices[device_id] = device

        await device.connect()
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        device = self.devices[device_id]
        await device.disconnect()
        del self.devices[device_id]

    async def send_message(self, message: Message) -> None:
        device = self.devices[message.device_id]

        await device.send_message(message.msg_type, message.data)
