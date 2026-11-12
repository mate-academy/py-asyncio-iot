import asyncio
from typing import Any, Awaitable

from iot.message import Message


class IOTService:
    def __init__(self) -> None:
        self.devices = {}
        self.device_id = 0

    async def register_device(self, device: Any) -> int:
        await device.connect()

        device_id = self.device_id
        self.devices[device_id] = device
        self.device_id += 1

        return device_id

    async def send_message(self, message: Message) -> None:
        device = self.devices[message.device_id]
        await device.send_message(message)

    async def disconnect_device(self, device_id: int) -> None:
        device = self.devices[device_id]
        await device.disconnect()


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)
