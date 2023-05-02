from asyncio import sleep

from .message import MessageType

TIME_TO_SLEEP = 0.5


class HueLightDevice:
    async def connect(self) -> None:
        print("Connecting Hue Light.")
        await sleep(TIME_TO_SLEEP)
        print("Hue Light connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Hue Light.")
        await sleep(TIME_TO_SLEEP)
        print("Hue Light disconnected.")

    async def send_message(self,
                           message_type: MessageType,
                           data: str = "") -> None:
        print(
            "Hue Light handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await sleep(TIME_TO_SLEEP)
        print("Hue Light received message.")


class SmartSpeakerDevice:
    async def connect(self) -> None:
        print("Connecting to Smart Speaker.")
        await sleep(TIME_TO_SLEEP)
        print("Smart Speaker connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")
        await sleep(TIME_TO_SLEEP)
        print("Smart Speaker disconnected.")

    async def send_message(self,
                           message_type: MessageType,
                           data: str = "") -> None:
        print(
            "Smart Speaker handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await sleep(TIME_TO_SLEEP)
        print("Smart Speaker received message.")


class SmartToiletDevice:
    async def connect(self) -> None:
        print("Connecting to Smart Toilet.")
        await sleep(TIME_TO_SLEEP)
        print("Smart Toilet connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Toilet.")
        await sleep(TIME_TO_SLEEP)
        print("Smart Toilet disconnected.")

    async def send_message(self,
                           message_type: MessageType,
                           data: str = "") -> None:
        print(
            "Smart Toilet handling message of type "
            f"{message_type.name} with data [{data}]."
        )
        await sleep(TIME_TO_SLEEP)
        print("Smart Toilet received message.")
