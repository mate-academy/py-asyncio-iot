import asyncio
from typing import Any, Awaitable, List
from app.iot.devices import Device


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


class IOTService:
    def __init__(self) -> None:
        self.devices: List[Device] = []

    async def register_device(self, device: Device) -> str:
        await device.connect()
        self.devices.append(device)
        return device.id

    async def unregister_device(self, device: Device) -> None:
        await device.disconnect()
        self.devices.remove(device)
