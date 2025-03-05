import asyncio
from .message import MessageType


TIME_TO_SLEEP = 0.5


class Device:
    def __init__(self, name: str) -> None:
        self.name = name

    async def connect(self) -> None:
        print(f"Connecting {self.name}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.name} connected.")

    async def disconnect(self) -> None:
        print(f"Disconnecting {self.name}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.name} disconnected.")

    async def send_message(
            self,
            message_type: MessageType,
            data: str = ""
    ) -> None:
        print(
            f"{self.name} handling message of type"
            f" {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.name} received message.")


class HueLightDevice(Device):
    def __init__(self, name: str = "Hue Light") -> None:
        super().__init__(name)


class SmartSpeakerDevice(Device):
    def __init__(self, name: str = "Smart Speaker") -> None:
        super().__init__(name)


class SmartToiletDevice(Device):
    def __init__(self, name: str = "Smart Toilet") -> None:
        super().__init__(name)
