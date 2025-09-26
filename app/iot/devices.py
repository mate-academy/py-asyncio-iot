import asyncio

from .message import MessageType

TIME_TO_SLEEP = 0.5


# of course this code looks dumb,
# but imagine some real implementations
# of each method here
class HueLightDevice:
    async def connect(self) -> None:
        await asyncio.to_thread(print, "Connecting Hue Light.")
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(print, "Hue Light connected.")

    async def disconnect(self) -> None:
        await asyncio.to_thread(print, "Disconnecting Hue Light.")
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Hue Light disconnected."
        )

    async def send_message(
            self,
            message_type: MessageType,
            data: str = "") -> None:
        await asyncio.to_thread(print,
                                f"Hue Light handling message"
                                f" of type {message_type.name} with "
                                f"data [{data}]."
                                )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Hue Light received message."
        )


class SmartSpeakerDevice:
    async def connect(self) -> None:
        await asyncio.to_thread(
            print,
            "Connecting to Smart Speaker."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Smart Speaker connected."
        )

    async def disconnect(self) -> None:
        await asyncio.to_thread(
            print,
            "Disconnecting Smart Speaker."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Smart Speaker disconnected."
        )

    async def send_message(
            self,
            message_type: MessageType,
            data: str = "") -> None:
        await asyncio.to_thread(print,
                                f"Smart Speaker handling message"
                                f" of type {message_type.name} with data"
                                f" [{data}]."
                                )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Smart Speaker received message."
        )


class SmartToiletDevice:
    async def connect(self) -> None:
        await asyncio.to_thread(
            print,
            "Connecting to Smart Toilet."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Smart Toilet connected."
        )

    async def disconnect(self) -> None:
        await asyncio.to_thread(
            print,
            "Disconnecting Smart Toilet."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Smart Toilet disconnected."
        )

    async def send_message(
            self,
            message_type: MessageType,
            data: str = "") -> None:
        await asyncio.to_thread(print,
                                f"Smart Toilet handling "
                                f"message of type {message_type.name} "
                                f"with data [{data}]."
                                )
        await asyncio.sleep(TIME_TO_SLEEP)
        await asyncio.to_thread(
            print,
            "Smart Toilet received message."
        )
