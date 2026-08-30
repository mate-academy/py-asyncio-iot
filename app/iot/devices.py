import asyncio

from iot.message import Message, MessageType


class HueLightDevice:
    def __init__(self) -> None:
        self.is_on = False

    async def connect(self) -> None:
        await asyncio.sleep(0.1)

    async def disconnect(self) -> None:
        await asyncio.sleep(0.1)

    async def send_message(self, message: Message) -> None:
        if message.message_type == MessageType.SWITCH_ON:
            self.is_on = True
        elif message.message_type == MessageType.SWITCH_OFF:
            self.is_on = False

        await asyncio.sleep(0.1)


class SmartSpeakerDevice:
    def __init__(self) -> None:
        self.is_on = False

    async def connect(self) -> None:
        await asyncio.sleep(0.1)

    async def disconnect(self) -> None:
        await asyncio.sleep(0.1)

    async def send_message(self, message: Message) -> None:
        if message.message_type == MessageType.SWITCH_ON:
            self.is_on = True
        elif message.message_type == MessageType.SWITCH_OFF:
            self.is_on = False
        elif message.message_type == MessageType.PLAY_SONG:
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.1)


class SmartToiletDevice:
    def __init__(self) -> None:
        self.is_on = False

    async def connect(self) -> None:
        await asyncio.sleep(0.1)

    async def disconnect(self) -> None:
        await asyncio.sleep(0.1)

    async def send_message(self, message: Message) -> None:
        if message.message_type == MessageType.FLUSH:
            await asyncio.sleep(0.1)
        elif message.message_type == MessageType.CLEAN:
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.1)
