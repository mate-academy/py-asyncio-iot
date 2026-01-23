from typing import Protocol
import asyncio
import random
import string
from collections import defaultdict

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def register_multiple_devices(
            self,
            devices: list[Device]
    ) -> list[str]:
        tasks = [self.register_device(device) for device in devices]
        return await asyncio.gather(*tasks)

    async def unregister_device(self, device_id: str) -> None:
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")

        device_messages: dict[str, list[Message]] = defaultdict(list)
        for msg in program:
            device_messages[msg.device_id].append(msg)

        async def run_device_msgs(msgs: list[Message]) -> None:
            for msg in msgs:
                await self.send_msg(msg)

        tasks = [run_device_msgs(msgs) for msgs in device_messages.values()]
        await asyncio.gather(*tasks)

        print("=====END OF PROGRAM======")
