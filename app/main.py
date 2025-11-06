import asyncio
import time
from typing import Any, Awaitable

# --- Helper Functions (as provided) ---

async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Runs a series of awaitable functions one after another."""
    print("... (Running tasks in SEQUENCE) ...")
    for function in functions:
        await function

async def run_parallel(*functions: Awaitable[Any]) -> None:
    """Runs a series of awaitable functions concurrently."""
    print("... (Running tasks in PARALLEL) ...")
    await asyncio.gather(*functions)

# --- Device and Service Definitions ---

class Device:
    """A simple class to represent an IoT device."""
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"Device(name='{self.name}')"

class IoTService:
    """
    The asynchronous IoT service.
    All I/O operations (connect, disconnect, send) are now non-blocking.
    """
    def __init__(self):
        self.devices = {}
        print("IoT Service initialized")

    async def register_device(self, device: Device):
        """Simulates the async registration of a device."""
        print(f"Registering {device.name}...")
        # Simulate non-blocking I/O (e.g., database write)
        await asyncio.sleep(1.0) 
        self.devices[device.name] = device
        print(f"✅ {device.name} registered.")

    async def connect(self, device: Device):
        """Simulates an async connection."""
        # print(f"Connecting to {device.name}...")
        await asyncio.sleep(0.1) # Simulate non-blocking I/O
        # print(f"{device.name} connected.")

    async def disconnect(self, device: Device):
        """Simulates an async disconnection."""
        # print(f"Disconnecting from {device.name}...")
        await asyncio.sleep(0.1) # Simulate non-blocking I/O
        # print(f"{device.name} disconnected.")

    async def send_message(self, device: Device, message: str):
        """
        Simulates the full, non-blocking process of sending a message:
        connect -> send -> disconnect
        """
        print(f"Sending to {device.name}: '{message}'")
        await self.connect(device)
        
        # Simulate the time taken for the command to execute
        await asyncio.sleep(0.5) 
        
        print(f"  -> {device.name} executed '{message}'")
        await self.disconnect(device)


# --- Main Application Logic ---

async def main():
    """
    The main asynchronous entry point for our IoT service.
    """
    main_start_time = time.time()
    service = IoTService()

    # Create device instances
    coffee_machine = Device("Smart Coffee Machine")
    speaker = Device("Smart Speaker")
    smart_toilet = Device("Smart Toilet")

    devices_to_register = [coffee_machine, speaker, smart_toilet]

    # --- Step 2: Register devices in parallel ---
    print("\n--- 1. Registering Devices ---")
    reg_start_time = time.time()
    
    # We use run_parallel to register all devices at the same time.
    # No device has to wait for another to finish registering.
    await run_parallel(
        *(service.register_device(d) for d in devices_to_register)
    )
    
    print(f"--- Devices registered in {time.time() - reg_start_time:.2f}s ---\n")


    # --- Step 3 & 4: Run programs with correct logic ---
    
    # As requested, the 'wake_up_program' and 'sleep_program' variables
    # are removed. We now directly call the service using our helper functions.

    print("--- 2. Running Wake Up Program ---")
    wake_up_start_time = time.time()

    # The individual device sequences *must* run in order.
    # e.g., You must "switch on" the speaker BEFORE "play music".
    
    # But the Speaker, Coffee Machine, and Toilet routines are
    # independent and can all happen at the same time.
    
    # We will run three *sequences* in *parallel*.
    
    await run_parallel(
        # Sequence 1: Speaker
        run_sequence(
            service.send_message(speaker, "switch on"),
            service.send_message(speaker, "play music")
        ),
        
        # Sequence 2: Coffee Machine
        run_sequence(
            service.send_message(coffee_machine, "switch on"),
            service.send_message(coffee_machine, "make coffee")
        ),
        
        # Sequence 3: Smart Toilet
        run_sequence(
            service.send_message(smart_toilet, "flush"),
            service.send_message(smart_toilet, "clean")
        )
    )

    print(f"--- Wake Up program finished in {time.time() - wake_up_start_time:.2f}s ---\n")


    print("--- 3. Running Sleep Program ---")
    sleep_start_time = time.time()

    # For the sleep program, all "switch off" commands are
    # independent. They can all be run in parallel.
    
    await run_parallel(
        service.send_message(speaker, "switch off"),
        service.send_message(coffee_machine, "switch off")
    )
    
    print(f"--- Sleep program finished in {time.time() - sleep_start_time:.2f}s ---\n")
    print(f"=== Total execution time: {time.time() - main_start_time:.2f}s ===")


if __name__ == "__main__":
    # In a synchronous world, this entire program would take
    # (1.0*3) for registration + (0.7*6) for wake-up + (0.7*2) for sleep
    # = 3.0 + 4.2 + 1.4 = 8.6 seconds (approx, given 0.1+0.5+0.1 per send)
    
    # With asyncio, the time is dominated by the *longest* parallel task.
    # Registration: max(1.0, 1.0, 1.0) = 1.0s
    # Wake Up: max(seq_speaker, seq_coffee, seq_toilet)
    #          max(0.7+0.7, 0.7+0.7, 0.7+0.7) = 1.4s
    # Sleep: max(0.7, 0.7) = 0.7s
    # Total expected: ~1.0 + 1.4 + 0.7 = 3.1 seconds.
    # This is a significant improvement!
    
    asyncio.run(main())
