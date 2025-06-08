import asyncio
import time
from typing import Any, Awaitable


# --- Helper functions ---
async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


# --- Simulated MessageType ---
class MessageType:
    SWITCH_ON = "switch_on"
    SWITCH_OFF = "switch_off"
    PLAY_SONG = "play_song"
    FLUSH = "flush"
    CLEAN = "clean"


# --- Base device class ---
class Device:
    async def send(self, msg_type: str, *args: Any) -> None:
        raise NotImplementedError


# --- Devices ---
class HueLightDevice(Device):
    async def send(self, msg_type: str, *args: Any) -> None:
        await asyncio.sleep(1)
        if msg_type == MessageType.SWITCH_ON:
            print("Hue Light: switched ON")
        elif msg_type == MessageType.SWITCH_OFF:
            print("Hue Light: switched OFF")


class SmartSpeakerDevice(Device):
    async def send(self, msg_type: str, *args: Any) -> None:
        await asyncio.sleep(1)
        if msg_type == MessageType.SWITCH_ON:
            print("Speaker: turned ON")
        elif msg_type == MessageType.SWITCH_OFF:
            print("Speaker: turned OFF")
        elif msg_type == MessageType.PLAY_SONG:
            print(f"Speaker: playing song — {args[0]}")


class SmartToiletDevice(Device):
    async def send(self, msg_type: str, *args: Any) -> None:
        await asyncio.sleep(1)
        if msg_type == MessageType.FLUSH:
            print("Toilet: flushing")
        elif msg_type == MessageType.CLEAN:
            print("Toilet: cleaning")


# --- Service ---
class IOTService:
    def __init__(self) -> None:
        self.devices: list[Device] = []
        self._lock = asyncio.Lock()  # Protect shared state

    async def register_device(self, device: Device) -> int:
        await asyncio.sleep(0.1)  # Simulate handshake
        async with self._lock:
            self.devices.append(device)
            return len(self.devices) - 1

    def get_device(self, device_id: int) -> Device:
        return self.devices[device_id]


# --- Main program ---
async def main() -> None:
    service = IOTService()

    # Devices to register
    devices = [
        HueLightDevice(),
        SmartSpeakerDevice(),
        SmartToiletDevice()
    ]

    # Parallel registration with unique ID assignment
    device_ids = await asyncio.gather(*[
        service.register_device(device) for device in devices
    ])

    light = service.get_device(device_ids[0])
    speaker = service.get_device(device_ids[1])
    toilet = service.get_device(device_ids[2])

    # Wake-up program
    await run_parallel(
        light.send(MessageType.SWITCH_ON),
        run_sequence(
            speaker.send(MessageType.SWITCH_ON),
            speaker.send(MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")
        )
    )

    # Sleep program
    await run_parallel(
        light.send(MessageType.SWITCH_OFF),
        speaker.send(MessageType.SWITCH_OFF),
        run_sequence(
            toilet.send(MessageType.FLUSH),
            toilet.send(MessageType.CLEAN)
        )
    )


# --- Entry point ---
if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"\nElapsed: {end - start:.2f} seconds")
