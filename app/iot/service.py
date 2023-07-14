import random
import string
import asyncio
from typing import Protocol, Awaitable, Any

from app.iot.message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


# Protocol is very similar to ABC, but uses duck typing
# so devices should not inherit for it (if it walks like a duck, and quacks like a duck, it's a duck)
class Device(Protocol):
    def connect(self) -> None:
        ...  # Ellipsis - similar to "pass", but sometimes has different meaning

    def disconnect(self) -> None:
        ...

    def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    def unregister_device(self, device_id: str) -> None:
        self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        if device_id in self.devices:
            return self.devices[device_id]
        else:
            raise ValueError(f"Device with id '{device_id}' is not registered.")

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        parallel_functions = []
        sequence_functions = []

        for msg in program:
            device = self.get_device(msg.device_id)
            message_type = msg.msg_type
            data = msg.data

            if message_type == MessageType.SWITCH_ON:
                parallel_functions.append(device.connect())
            elif message_type == MessageType.SWITCH_OFF:
                parallel_functions.append(device.disconnect())
            elif message_type == MessageType.FLUSH:
                sequence_functions.append(device.send_message(message_type, data))
            elif message_type == MessageType.CLEAN:
                sequence_functions.append(device.send_message(message_type, data))
            else:
                parallel_functions.append(self.send_msg(msg))

        await run_sequence(*sequence_functions)
        await run_parallel(*parallel_functions)

        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        device = self.get_device(msg.device_id)
        await device.send_message(msg.msg_type, msg.data)
