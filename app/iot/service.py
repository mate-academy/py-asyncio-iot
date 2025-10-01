import asyncio
import random
import string
from typing import Protocol
from typing import Any, Awaitable
from app.iot.message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


# Protocol is very similar to ABC, but uses duck typing
# so devices should not inherit for it
# (if it walks like a duck, and quacks like a duck, it's a duck)
class Device(Protocol):
    async def connect(self) -> None:
        ...  # Ellipsis - similar to "pass",
        # but sometimes has different meaning

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

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")
        if not program:
            raise ValueError("program must not be empty")

        if program[0].msg_type == MessageType.SWITCH_ON:
            light_on, speaker_on, play_song = program
            await run_parallel(
                self.send_msg(light_on),
                run_sequence(
                    self.send_msg(speaker_on),
                    self.send_msg(play_song),
                ),
            )

        elif program[0].msg_type == MessageType.SWITCH_OFF:
            light_off, speaker_off, flush, clean = program
            await run_parallel(
                self.send_msg(light_off),
                self.send_msg(speaker_off),
                run_sequence(
                    self.send_msg(flush),
                    self.send_msg(clean),
                ),
            )

        else:
            print("ERROR: Unknown type of program")

        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
