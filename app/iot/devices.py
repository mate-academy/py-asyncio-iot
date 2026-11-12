import asyncio
from app.iot.message import MessageType


class Device:
    def __init__(self, device_id: str) -> None:
        self.id = device_id

    async def connect(self) -> None:
        await asyncio.sleep(0.5)

    async def disconnect(self) -> None:
        await asyncio.sleep(0.5)

    async def send_message(
        self, message_type: MessageType, data: str = ""
    ) -> None:
        await asyncio.sleep(0.5)
        msg_val = message_type.value
        out = f"Device {self.id} received message: {msg_val} {data}".strip()
        print(out)
