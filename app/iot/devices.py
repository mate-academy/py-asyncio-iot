import asyncio
from typing import Any
from enum import Enum, auto


# Mock MessageType for completeness
class MessageType(Enum):
    SWITCH_ON = auto()
    SWITCH_OFF = auto()
    PLAY_AUDIO = auto()
    FLUSH = auto()


class IoTDevice:
    """Standardized asynchronous base class for all IoT devices."""
    def __init__(self, name: str) -> None:
        self.name = name

    async def connect(self) -> None:
        print(self._log("Connecting..."))
        await asyncio.sleep(0.5)
        print(self._log("Connected."))

    async def disconnect(self) -> None:
        print(self._log("Disconnecting..."))
        await asyncio.sleep(0.2)
        print(self._log("Disconnected."))

    async def send_message(self, command: str, payload: Any = None) -> None:
        print(self._log(self._format_msg(command, payload)))
        await asyncio.sleep(0.3)

    def _log(self, text: str) -> str:
        return f"[{self.name}] {text}"

    def _format_msg(self, command: str, payload: Any) -> str:
        return f"Sending command -> {command} (Payload: {payload})" \
            if payload else f"Sending command -> {command}"


# Clean, non-duplicated concrete implementations
class HueLightDevice(IoTDevice):
    def __init__(self) -> None:
        super().__init__("Hue Light")


class SmartSpeakerDevice(IoTDevice):
    def __init__(self) -> None:
        super().__init__("Smart Speaker")


class SmartToiletDevice(IoTDevice):
    def __init__(self) -> None:
        super().__init__("Smart Toilet")
