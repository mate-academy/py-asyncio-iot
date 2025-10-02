import asyncio
from typing import Iterable, Any, Mapping

from app.iot.devices import BaseDevice, Light, Speaker, SmartToilet, CoffeeMaker
from app.iot.message import MessageType


class IoTService:
    def __init__(self) -> None:
        # device_id -> device
        self._devices: dict[str, BaseDevice] = {}

    async def register_device(self, device: BaseDevice) -> str:
        """Реєструє один пристрій і повертає його device_id."""
        await device.connect()
        device_id = device.name  # стабільний id = ім’я
        self._devices[device_id] = device
        return device_id

    async def register_devices(self, devices: Iterable[BaseDevice]) -> list[str]:
        """
        Реєструє кілька пристроїв ПАРАЛЕЛЬНО.
        ВАЖЛИВО: перетворюємо на list, щоб безпечно ітерувати двічі
        (gather + заповнення реєстру), навіть якщо на вхід прийде генератор.
        """
        devices = list(devices)
        await asyncio.gather(*(d.connect() for d in devices))
        ids: list[str] = []
        for d in devices:
            device_id = d.name
            self._devices[device_id] = d
            ids.append(device_id)
        return ids

    async def send_message(self, message: Any) -> None:
        """
        Гнучкий парсер повідомлень:
          - Підтримує об’єктні повідомлення (атрибути) і mapping (dict).
          - Поля: device_id/device/id; type/message_type/msg_type; payload/data/value.
          - type може бути Enum (MessageType) або рядком ("SWITCH_ON", "flush", ...).
        Дає зрозумілу помилку, якщо пристрій не зареєстрований.
        """
        # 1) Дістаємо поля з message (attr або mapping)
        if isinstance(message, Mapping):
            device_id = message.get("device_id") or message.get("device") or message.get("id")
            msg_type = message.get("type") or message.get("message_type") or message.get("msg_type")
            payload = message.get("payload") or message.get("data") or message.get("value")
        else:
            device_id = (
                getattr(message, "device_id", None)
                or getattr(message, "device", None)
                or getattr(message, "id", None)
            )
            msg_type = (
                getattr(message, "type", None)
                or getattr(message, "message_type", None)
                or getattr(message, "msg_type", None)
            )
            payload = (
                getattr(message, "payload", None)
                or getattr(message, "data", None)
                or getattr(message, "value", None)
            )

        if device_id is None:
            raise ValueError("Message missing device_id/device/id")
        if msg_type is None:
            raise ValueError("Message missing type/message_type/msg_type")

        # 2) Валідуємо наявність пристрою
        device = self._devices.get(device_id)
        if device is None:
            raise ValueError(f"Device {device_id!r} is not registered")

        # 3) Нормалізуємо тип у УСЯКОМУ форматі -> до верхнього регістру рядка
        def normalize_type(mt: Any) -> str:
            if isinstance(mt, MessageType):
                # краще name, але якщо нема — падати не будемо
                name = getattr(mt, "name", None)
                return name or str(getattr(mt, "value", mt)).upper()
            if hasattr(mt, "name"):
                return str(mt.name).upper()
            if hasattr(mt, "value") and not isinstance(mt, (str, bytes)):
                return str(mt.value).upper()
            return str(mt).upper()

        mt_name = normalize_type(msg_type)

        # 4) МАПА типів → конкретні команди, які очікують пристрої (devices.py)
        if isinstance(device, Light):
            if mt_name in ("SWITCH_ON", "ON"):
                cmd, pl = "on", None
            elif mt_name in ("SWITCH_OFF", "OFF"):
                cmd, pl = "off", None
            else:
                cmd, pl = mt_name.lower(), payload

        elif isinstance(device, Speaker):
            if mt_name in ("SWITCH_ON", "POWER_ON"):
                cmd, pl = "power_on", None
            elif mt_name in ("SWITCH_OFF", "POWER_OFF"):
                cmd, pl = "power_off", None
            elif mt_name in ("PLAY_SONG", "PLAY"):
                cmd, pl = "play", payload
            elif mt_name in ("STOP_SONG", "STOP"):
                cmd, pl = "stop", None
            else:
                cmd, pl = mt_name.lower(), payload

        elif isinstance(device, SmartToilet):
            if mt_name == "FLUSH":
                cmd, pl = "flush", None
            elif mt_name == "CLEAN":
                cmd, pl = "clean", None
            else:
                cmd, pl = mt_name.lower(), payload

        elif isinstance(device, CoffeeMaker):
            if mt_name in ("BREW", "MAKE_COFFEE"):
                cmd, pl = "brew", None
            else:
                cmd, pl = mt_name.lower(), payload

        else:
            cmd, pl = mt_name.lower(), payload

        # 5) Власне виконання команди на пристрої
        await device.handle(cmd, pl)

    async def disconnect_all(self) -> None:
        await asyncio.gather(*(d.disconnect() for d in self._devices.values()))
