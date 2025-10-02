import asyncio
import time

from app.iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from app.iot.message import Message, MessageType
from app.iot.service import IoTService
from app.iot.utils import run_parallel, run_sequence


async def async_main() -> None:
    service = IoTService()

    # створюємо девайси З ІМЕНАМИ (узгоджено з BaseDevice)
    hue_light = HueLightDevice("HueLight")
    speaker = SmartSpeakerDevice("SmartSpeaker")
    toilet = SmartToiletDevice("SmartToilet")

    # реєструємо ПАРАЛЕЛЬНО (і отримуємо id — тут це ті самі імена)
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # === WAKE-UP PROGRAM ===
    # Паралельно: увімкнути світло і спікер
    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_ON)),
        service.send_message(Message(speaker_id, MessageType.SWITCH_ON)),
    )
    # Після увімкнення — послідовно програти трек
    await run_sequence(
        service.send_message(
            Message(
                speaker_id,
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up",
            )
        )
    )

    # === SLEEP PROGRAM ===
    # Паралельно: вимкнути світло; унітаз — послідовно flush -> clean;
    # спікер — спочатку STOP_SONG (якщо є), потім SWITCH_OFF (послідовно).
    stop_song_step = []
    if hasattr(MessageType, "STOP_SONG"):
        stop_song_step.append(
            service.send_message(Message(speaker_id, MessageType.STOP_SONG))
        )

    await run_parallel(
        service.send_message(Message(hue_light_id, MessageType.SWITCH_OFF)),
        run_sequence(
            service.send_message(Message(toilet_id, MessageType.FLUSH)),
            service.send_message(Message(toilet_id, MessageType.CLEAN)),
        ),
        run_sequence(
            *(stop_song_step or []),
            service.send_message(Message(speaker_id, MessageType.SWITCH_OFF)),
        ),
    )

    # Акуратно вимкнути всі девайси перед виходом (graceful shutdown)
    await service.disconnect_all()


def main() -> None:
    start = time.perf_counter()
    asyncio.run(async_main())
    end = time.perf_counter()
    print("Elapsed:", end - start)


if __name__ == "__main__":
    main()
