import random
import string
import asyncio
from typing import Protocol, Awaitable, Any

from app.iot.message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing
# so devices should not inherit for it
# (if it walks like a duck, and quacks like a duck, it's a duck)
class Device(Protocol):
    async def connect(self) -> None:
        ...
        # Ellipsis - similar to "pass", but sometimes has different meaning

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

    async def unregister_device(self, device_id: str) -> None:
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_sequence(self, *functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(self, *functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        flush_clean = [
            msg for msg in program
            if msg.msg_type in {MessageType.FLUSH, MessageType.CLEAN}
        ]
        other_commands = [
            msg for msg in program
            if msg.msg_type not in {MessageType.FLUSH, MessageType.CLEAN}
        ]

        if flush_clean:
            await asyncio.gather(
                *(self.send_msg(msg) for msg in other_commands),
                self.run_sequence(*(self.send_msg(msg) for msg in flush_clean))
            )
        else:
            await asyncio.gather(
                *(self.send_msg(msg) for msg in other_commands)
            )
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
