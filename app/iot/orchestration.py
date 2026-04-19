import asyncio


async def run_sequence(*args):
    for arg in args:
        await arg


async def run_parallel(*args):
    await asyncio.gather(*args)
