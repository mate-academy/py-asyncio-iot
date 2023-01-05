import asyncio

from .message import MessageType


class HomeDevice:
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

    async def send_message(
            self,
            message_type: MessageType,
            data: str = ""
    ) -> None:
        print(
            f"{self.DEVICE_NAME} message of type "
            f"{message_type.name} with data [{data}]."
        )
        await asyncio.sleep(self.TIME_TO_SLEEP)
        print(f"{self.DEVICE_NAME} received message.")


class HueLightDevice(HomeDevice):
    DEVICE_NAME = "Hue Light"


class SmartSpeakerDevice(HomeDevice):
    DEVICE_NAME = "Speaker"


class SmartToiletDevice(HomeDevice):
    DEVICE_NAME = "Toilet"
