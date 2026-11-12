import asyncio

from .message import MessageType


TIME_TO_SLEEP = 0.5


class DeviceItem:
    NAME = ""

    async def connect(self) -> None:
        print(f"Connecting {self.NAME}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.NAME} connected.")

    async def disconnect(self) -> None:
        print(f"Disconnecting {self.NAME}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.NAME} disconnected.")

    async def send_message(
            self,
            message_type: MessageType,
            data: str = ""
    ) -> None:
        print(
            f"{self.NAME} handling message "
            f"of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.NAME} received message.")


# of course this code looks dumb,
# but imagine some real implementations of each method here
class HueLightDevice(DeviceItem):
    NAME = "Hue Light"


class SmartSpeakerDevice(DeviceItem):
    NAME = "Smart Speaker"


class SmartToiletDevice(DeviceItem):
    NAME = "Smart Toilet"
