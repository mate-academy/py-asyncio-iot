from dataclasses import dataclass
from enum import Enum, auto


class MessageType(Enum):
    """
    Enumeration of possible message types that can be sent to IoT devices.

    Defines the various commands that IoT devices can receive and process.
    """

    SWITCH_ON = auto()
    SWITCH_OFF = auto()
    CHANGE_COLOR = auto()
    PLAY_SONG = auto()
    OPEN = auto()
    CLOSE = auto()
    FLUSH = auto()
    CLEAN = auto()


@dataclass
class Message:
    """A message that can be sent to an IoT device."""

    device_id: str
    msg_type: MessageType
    data: str = ""
