import time
import asyncio

from .message import MessageType


TIME_TO_SLEEP = 0.5


# of course this code looks dumb, but imagine some real implementations of each method here
class HueLightDevice:
    async def connect(self) -> None:
        print("Connecting Hue Light.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Hue Light connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Hue Light.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Hue Light disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Hue Light handling message of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Hue Light received message.")


class SmartSpeakerDevice:
    def connect(self) -> None:
        print("Connecting to Smart Speaker.")
        time.sleep(TIME_TO_SLEEP)
        print("Smart Speaker connected.")

    def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")
        time.sleep(TIME_TO_SLEEP)
        print("Smart Speaker disconnected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )
        time.sleep(TIME_TO_SLEEP)
        print("Smart Speaker received message.")


class SmartToiletDevice:
    def connect(self) -> None:
        print("Connecting to Smart Toilet.")
        time.sleep(TIME_TO_SLEEP)
        print("Smart Toilet connected.")

    def disconnect(self) -> None:
        print("Disconnecting Smart Toilet.")
        time.sleep(TIME_TO_SLEEP)
        print("Smart Toilet disconnected.")

    def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Toilet handling message of type {message_type.name} with data [{data}]."
        )
        time.sleep(TIME_TO_SLEEP)
        print("Smart Toilet received message.")
