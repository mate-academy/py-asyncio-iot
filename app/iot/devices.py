import asyncio
import httpx

from typing import Any, Awaitable

from .message import MessageType


TIME_TO_SLEEP = 0.5


# of course this code looks dumb, but imagine some real implementations of each method here
class HueLightDevice:
    async def connect(self, url: str, client: httpx.AsyncClient) -> None:
        print("Connecting Hue Light.")
        await client.get(url)
        print("Hue Light connected.")

    async def disconnect(self, url: str,  client: httpx.AsyncClient) -> None:
        print("Disconnecting Hue Light.")
        await client.get(url)
        print("Hue Light disconnected.")

    async def send_message(self, url: str,  message_type: MessageType, client: httpx.AsyncClient, data: str = "") -> None:
        print(
            f"Hue Light handling message of type {message_type.name} with data [{data}]."
        )
        await client.get(url)
        print("Hue Light received message.")


class SmartSpeakerDevice:
    async def connect(self, url: str,  client: httpx.AsyncClient) -> None:
        print("Connecting to Smart Speaker.")
        await client.get(url)
        print("Smart Speaker connected.")

    async def disconnect(self, url: str,  client: httpx.AsyncClient) -> None:
        print("Disconnecting Smart Speaker.")
        await client.get(url)
        print("Smart Speaker disconnected.")

    async def send_message(self, message_type: MessageType, url: str,  client: httpx.AsyncClient, data: str = "") -> None:
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )
        await client.get(url)
        print("Smart Speaker received message.")


class SmartToiletDevice:
    async def connect(self, url: str,  client: httpx.AsyncClient) -> None:
        print("Connecting to Smart Toilet.")
        await client.get(url)
        print("Smart Toilet connected.")

    async def disconnect(self, url: str,  client: httpx.AsyncClient) -> None:
        print("Disconnecting Smart Toilet.")
        await client.get(url)
        print("Smart Toilet disconnected.")

    async def send_message(self, message_type: MessageType, url: str,  client: httpx.AsyncClient, data: str = "") -> None:
        print(
            f"Smart Toilet handling message of type {message_type.name} with data [{data}]."
        )
        await client.get(url)
        print("Smart Toilet received message.")


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)