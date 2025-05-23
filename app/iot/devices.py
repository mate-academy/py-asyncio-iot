import asyncio
from abc import ABC

from .message import MessageType

TIME_TO_SLEEP = 0.5


class DeviceABC(ABC):
    name: str

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
        print(f"{self.name} handling message of type "
              f"{message_type.name} with data [{data}].")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.name} received message.")


# of course this code looks dumb, but imagine some
# real implementations of each method here
class HueLightDevice(DeviceABC):
    name = "Hue Light"


class SmartSpeakerDevice(DeviceABC):
    name = "Smart Speaker"


class SmartToiletDevice(DeviceABC):
    name = "Smart Toilet"
