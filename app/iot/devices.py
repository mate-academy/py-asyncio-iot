import asyncio
from .message import MessageType


class Device:
    TIME_TO_SLEEP = 0.5
    DEVICE_NAME = None

    async def connect(self) -> None:
        print(f"Connecting {self.DEVICE_NAME}.")
        await asyncio.sleep(self.TIME_TO_SLEEP)
        print(f"{self.DEVICE_NAME} connected.")

    async def disconnect(self) -> None:
        print(f"Disconnecting {self.DEVICE_NAME}.")
        await asyncio.sleep(self.TIME_TO_SLEEP)
        print(f"{self.DEVICE_NAME} disconnected.")

    async def send_message(self, message_type: MessageType,
                           data: str = "") -> None:
        print(
            f"{self.DEVICE_NAME} handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await asyncio.sleep(self.TIME_TO_SLEEP)
        print(f"{self.DEVICE_NAME} received message.")


class HueLightDevice(Device):
    DEVICE_NAME = "Hue Light"


class SmartSpeakerDevice(Device):
    DEVICE_NAME = "Smart Speaker"


class SmartToiletDevice(Device):
    DEVICE_NAME = "Smart Toilet"
