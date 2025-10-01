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
    async def connect(self) -> None:
        print("Connecting to Smart Speaker.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Speaker received message.")


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
        print(
            f"Smart Toilet handling message of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(TIME_TO_SLEEP)
        print("Smart Toilet received message.")


async def run_device(device, msg_type: MessageType, msg: str):
    await device.connect()
    await device.send_message(msg_type, msg)
    await device.disconnect()


async def main() -> None:
    light_device = HueLightDevice()
    speaker_device = SmartSpeakerDevice()
    toilet_device = SmartToiletDevice()

    await asyncio.gather(
        run_device(light_device, MessageType.SWITCH_ON, "Turn On"),
        run_device(speaker_device, MessageType.PLAY_SONG, "Play music"),
        run_device(toilet_device, MessageType.FLUSH, "Flush"),
    )
