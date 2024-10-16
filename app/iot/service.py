import random
import string
from typing import Protocol

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing
# so devices should not inherit for it (if it walks like a duck, and quacks like a duck, it's a duck)
class Device(Protocol):
    def connect(self) -> None:
        ...  # Ellipsis - similar to "pass", but sometimes has different meaning

    def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        await device.connect()
        device_id = generate_id()
        attempts_left = 7
        while device_id in self.devices:
            print(
                f"Device with id {device_id} already registered"
                f"Gererating new one..."
            )
            device_id = generate_id()
            attempts_left -= 1
            if attempts_left == 0:
                print("Unable to register device, trying again...")
            print(f"Attempts left: {attempts_left}")
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        try:
            self.devices[device_id].disconnect()
            del self.devices[device_id]
        except KeyError:
            print(f"Device {device_id} not found")


    async def get_device(self, device_id: str) -> Device:
        try:
            return self.devices.get(device_id)
        except AttributeError:
            print(f"Device {device_id} not found")


    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        for msg in program:
           await self.send_msg(msg)
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
       try:
           await self.devices.get(msg.device_id).send_message(msg.msg_type, msg.data)
       except AttributeError:
           print("Device not found")
