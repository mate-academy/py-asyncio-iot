import random
import string
from typing import Protocol
from typing import Tuple
import asyncio


from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol is very similar to ABC, but uses duck typing

class Device(Protocol):
    async def connect(self) -> None:
        ...  # Ellipsis - similar to "pass", but sometimes
        # has different meaning

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        # await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    def unregister_device(self, device_id: str) -> None:
        self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_program(self, program: list[Tuple[Device, Message]]) -> None:
        print("=====RUNNING PROGRAM======")
        # await asyncio.gather(*(device.send_message(message.message_type,
        #                                            message.data)
        #                        for device, message in program))
        # print("=====END OF PROGRAM======")
        # try:
        #     await asyncio.gather(
        #         *(device.send_message(message.message_type, message.data)
        #         for device, message in program))
        # except Exception as e:
        #     print(f"An error occurred during program execution: {e}")
        # else:
        #     print("=====END OF PROGRAM======")
        messages = [(self.get_device(msg.device_id), msg) for msg in program]
        try:
            await asyncio.gather(
                *(device.send_message(message.msg_type, message.data)
                  for device, message in messages))
        except Exception as e:
            print(f"An error occurred during program execution: {e}")
        else:
            print("=====END OF PROGRAM======")

    def send_msg(self, msg: Message) -> Tuple[Device, Message]:
        self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
