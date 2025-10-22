import asyncio
from typing import Any


class BaseDevice:
    """Базовий пристрій IoT з асинхронними операціями."""
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        self._connected = False

    async def connect(self) -> None:
        """Емуляція дорогого підключення."""
        await asyncio.sleep(0.1)
        self._connected = True
        print(f"[{self.name}] connected")

    async def disconnect(self) -> None:
        """Емуляція відключення."""
        await asyncio.sleep(0.05)
        self._connected = False
        print(f"[{self.name}] disconnected")

    async def handle(self, command: str, payload: Any | None = None) -> None:
        """
        Обробка команди (перевизначається у підкласах).
        Команди погоджені з service.send_message():
          Light:       'on', 'off'
          Speaker:     'power_on', 'power_off', 'play', 'stop'
          SmartToilet: 'flush', 'clean'
          CoffeeMaker: 'brew'
        """
        await asyncio.sleep(0.01)
        print(f"[{self.name}] command={command} payload={payload}")


class Speaker(BaseDevice):
    def __init__(self, name: str = "Speaker") -> None:
        super().__init__(name)
        self.power = False
        self.playing = False

    async def handle(self, command: str, payload: Any | None = None) -> None:
        await asyncio.sleep(0.05)
        if command == "power_on":
            self.power = True
            print(f"[{self.name}] powered ON")
        elif command == "power_off":
            self.power = False
            self.playing = False
            print(f"[{self.name}] powered OFF")
        elif command == "play":
            if not self.power:
                print(f"[{self.name}] ERROR: cannot play, power is OFF")
            else:
                self.playing = True
                print(f"[{self.name}] playing: {payload or 'track'}")
        elif command == "stop":
            self.playing = False
            print(f"[{self.name}] stopped")
        else:
            await super().handle(command, payload)


class SmartToilet(BaseDevice):
    async def handle(self, command: str, payload: Any | None = None) -> None:
        if command == "flush":
            await asyncio.sleep(0.15)
            print(f"[{self.name}] flushed")
        elif command == "clean":
            await asyncio.sleep(0.2)
            print(f"[{self.name}] cleaned")
        else:
            await super().handle(command, payload)


class Light(BaseDevice):
    def __init__(self, name: str = "Light") -> None:
        super().__init__(name)
        self.on = False

    async def handle(self, command: str, payload: Any | None = None) -> None:
        await asyncio.sleep(0.03)
        if command == "on":
            self.on = True
            print(f"[{self.name}] ON")
        elif command == "off":
            self.on = False
            print(f"[{self.name}] OFF")
        else:
            await super().handle(command, payload)


class CoffeeMaker(BaseDevice):
    async def handle(self, command: str, payload: Any | None = None) -> None:
        if command == "brew":
            await asyncio.sleep(0.25)
            print(f"[{self.name}] coffee is ready")
        else:
            await super().handle(command, payload)


# === Aliases to match imports used in the original skeleton/main ===

class HueLightDevice(Light):
    """Alias for backward compatibility with the task skeleton."""
    pass


class SmartSpeakerDevice(Speaker):
    """Alias for backward compatibility with the task skeleton."""
    pass


class SmartToiletDevice(SmartToilet):
    """Alias for backward compatibility with the task skeleton."""
    pass
