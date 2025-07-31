import asyncio
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> list[Any]:
    result = []
    for function in functions:
        result.append(await function)
    return result


async def run_parallel(*functions: Awaitable[Any]) -> list[Any]:
    return await asyncio.gather(*functions)
