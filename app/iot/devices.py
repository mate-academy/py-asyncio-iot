import asyncio

from app.iot.message import MessageType


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
        print("Hue Light received message.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(
            f"Hue Light handling message of type {message_type.name} with data [{data}]."
        )


class SmartSpeakerDevice:
    async def connect(self) -> None:
        print("Connecting to Smart Speaker.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print("Smart Speaker received message.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )


class SmartToiletDevice:
    async def connect(self) -> None:
        print("Connecting to Smart Toilet.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Toilet connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Toilet.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Toilet disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print("Smart Toilet received message.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print(
            f"Smart Toilet handling message of type {message_type.name} with data [{data}]."
        )
