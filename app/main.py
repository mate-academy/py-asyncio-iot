# app/iot/main.py
import asyncio
import time

from iot.service import orchestrate


def _run() -> None:
    asyncio.run(orchestrate())


if __name__ == "__main__":
    start = time.perf_counter()
    _run()
    end = time.perf_counter()
    print("Elapsed:", end - start)
