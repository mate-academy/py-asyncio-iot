import asyncio

from .message import MessageType


TIME_TO_SLEEP = 0.5


class SmartDevice:
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
        data: str = "",
    ) -> None:
        print(
            f"{self.name} handling message "
            f"of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.name} received message.")


class HueLightDevice(SmartDevice):
    def __init__(self) -> None:
        super().__init__("Hue Light")


class SmartSpeakerDevice(SmartDevice):
    def __init__(self) -> None:
        super().__init__("Smart Speaker")


class SmartToiletDevice(SmartDevice):
    def __init__(self) -> None:
        super().__init__("Smart Toilet")
