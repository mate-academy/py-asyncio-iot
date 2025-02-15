import asyncio

from .message import MessageType


TIME_TO_SLEEP = 0.5


class Device:
    def __init__(self, device_name: str) -> None:
        self.device_name = device_name

    async def connect(self) -> None:
        print(f"Connecting {self.device_name}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.device_name} connected.")

    async def disconnect(self) -> None:
        print(f"Disconnecting {self.device_name}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.device_name} disconnected.")

    async def send_message(
            self,
            message_type: MessageType,
            data: str = ""
    ) -> None:

        print(
            f"{self.device_name} handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.device_name} received message.")


class HueLightDevice(Device):
    def __init__(self) -> None:
        super().__init__("Hue Light")


class SmartSpeakerDevice(Device):
    def __init__(self) -> None:
        super().__init__("Smart Speaker")


class SmartToiletDevice(Device):
    def __init__(self) -> None:
        super().__init__("Smart Toilet")
