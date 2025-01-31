import random
import string
from typing import Any, Coroutine, Protocol
import asyncio


from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def send_message(self, message_type: MessageType, data: str) -> None:
        pass


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    def register_device(self, device: Device) -> str:
        device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    def unregister_device(self, device_id: str) -> None:
        self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        for msg in program:
            self.send_msg(msg)
        print("=====END OF PROGRAM======")

    def send_msg(self, msg: Message) -> None:
        self.devices[msg.device_id].send_message(msg.msg_type, msg.data)

    def wrap_send_msg_to_thread(
        self, msg: Message
    ) -> Coroutine[Any, Any, None]:
        return asyncio.to_thread(self.send_msg, msg)
