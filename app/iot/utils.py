import asyncio
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for fn in functions:
        await fn


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)
