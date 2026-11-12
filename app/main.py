import asyncio
from app.iot.devices import Device
from app.iot.message import MessageType
from app.iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    service = IOTService()

    hue_light = Device("hue_light")
    speaker = Device("speaker")
    smart_toilet = Device("smart_toilet")

    # Регистрируем устройства параллельно
    await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(smart_toilet),
    )

    # Программа "Wake up"
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_ON),
        run_sequence(
            speaker.send_message(MessageType.SWITCH_ON),
            speaker.send_message(
                MessageType.PLAY_SONG, "Meyers, Howard and Smith"
            ),
        ),
    )

    # Программа "Sleep"
    await run_parallel(
        hue_light.send_message(MessageType.SWITCH_OFF),
        speaker.send_message(MessageType.SWITCH_OFF),
        run_sequence(
            smart_toilet.send_message(MessageType.FLUSH),
            smart_toilet.send_message(MessageType.CLEAN),
        ),
    )

    # Отключаем устройства параллельно
    await run_parallel(
        service.unregister_device(hue_light),
        service.unregister_device(speaker),
        service.unregister_device(smart_toilet),
    )


if __name__ == "__main__":
    asyncio.run(main())
