import asyncio
from abc import ABC, abstractmethod

from .message import MessageType


TIME_TO_SLEEP = 0.5


class BaseDevice(ABC):
    """Base class for all IoT devices."""

    @property
    @abstractmethod
    def device_name(self) -> str:
        """Return the name of the device."""
        pass

    async def connect(self) -> None:
        """Connect the device."""
        print(f"Connecting to {self.device_name}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.device_name} connected.")

    async def disconnect(self) -> None:
        """Disconnect the device."""
        print(f"Disconnecting {self.device_name}.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.device_name} disconnected.")

    async def send_message(
        self, message_type: MessageType, data: str = ""
    ) -> None:
        """Handle message sending for the device."""
        print(
            f"{self.device_name} handling message of type {message_type.name} "
            f"with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print(f"{self.device_name} received message.")


class HueLightDevice(BaseDevice):
    """A smart light device that can be controlled remotely."""

    @property
    def device_name(self) -> str:
        return "Hue Light"


class SmartSpeakerDevice(BaseDevice):
    """A smart speaker device that can be controlled remotely."""

    @property
    def device_name(self) -> str:
        return "Smart Speaker"


class SmartToiletDevice(BaseDevice):
    """A smart toilet device that can be controlled remotely."""

    @property
    def device_name(self) -> str:
        return "Smart Toilet"
