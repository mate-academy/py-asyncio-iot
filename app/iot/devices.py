import asyncio

from .message import MessageType


TIME_TO_SLEEP = 0.5


class HueLightDevice:
    @staticmethod
    async def connect() -> None:
        print("Connecting Hue Light.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Hue Light connected.")

    @staticmethod
    async def disconnect() -> None:
        print("Disconnecting Hue Light.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Hue Light disconnected.")

    @staticmethod
    async def send_message(
            message_type: MessageType,
            data: str = ""
    ) -> None:
        print(
            "Hue Light handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Hue Light received message.")


class SmartSpeakerDevice:

    @staticmethod
    async def connect() -> None:
        print("Connecting to Smart Speaker.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker connected.")

    @staticmethod
    async def disconnect() -> None:
        print("Disconnecting Smart Speaker.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker disconnected.")

    @staticmethod
    async def send_message(
            message_type: MessageType,
            data: str = ""
    ) -> None:
        print(
            "Smart Speaker handling message of "
            f"type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker received message.")


class SmartToiletDevice:

    @staticmethod
    async def connect() -> None:
        print("Connecting to Smart Toilet.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Toilet connected.")

    @staticmethod
    async def disconnect() -> None:
        print("Disconnecting Smart Toilet.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Toilet disconnected.")

    @staticmethod
    async def send_message(
            message_type: MessageType,
            data: str = ""
    ) -> None:
        print(
            "Smart Toilet handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Toilet received message.")
