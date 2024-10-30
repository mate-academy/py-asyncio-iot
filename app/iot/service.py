import asyncio
import random
import string
from typing import Protocol

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


# Protocol визначає загальний інтерфейс для пристроїв, але без необхідності успадковування
class Device(Protocol):
    async def connect(self) -> None:
        ...  # Еліпсис означає, що метод повинен бути реалізований у класі пристрою

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


class IOTService:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        # Викликає асинхронний метод `connect` для підключення пристрою
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        # Викликає асинхронний метод `disconnect` для відключення пристрою
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        print("=====RUNNING PROGRAM======")

        # Створюємо завдання для кожного повідомлення у програмі
        tasks = [self.send_message(msg) for msg in program]

        # Запускаємо всі завдання одночасно для швидшого виконання
        await asyncio.gather(*tasks)

        print("=====END OF PROGRAM======")

    async def send_message(self, msg: Message) -> None:
        # Відправляє повідомлення на основі типу і даних
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
