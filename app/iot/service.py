import asyncio
import random
import string
from typing import Protocol

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

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def register_devices(self, *devices: Device) -> list[str]:
        connect_tasks = [device.connect() for device in devices]
        await asyncio.gather(*connect_tasks)

        device_ids = []
        for device in devices:
            device_id = generate_id()
            self.devices[device_id] = device
            device_ids.append(device_id)

        return device_ids

    async def unregister_device(self, device_id: str) -> None:
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    async def unregister_devices(self, *device_ids: str) -> None:
        disconnect_tasks = [self.devices[device_id].disconnect() for device_id in device_ids]
        await asyncio.gather(*disconnect_tasks)

        for device_id in device_ids:
            del self.devices[device_id]

    async def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")

        device_messages = {}
        for msg in program:
            if msg.device_id not in device_messages:
                device_messages[msg.device_id] = []
            device_messages[msg.device_id].append(msg)

        async def process_device_messages(device_id: str, messages: list[Message]):
            for msg in messages:
                await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)

        tasks = [process_device_messages(device_id, messages)
                 for device_id, messages in device_messages.items()]
        await asyncio.gather(*tasks)

        print("=====END OF PROGRAM======")

    async def run_programs(self, *programs: list[Message]) -> None:
        tasks = [self.run_program(program) for program in programs]
        await asyncio.gather(*tasks)

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
