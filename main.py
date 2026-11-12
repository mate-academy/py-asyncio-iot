import asyncio
from iot.device import Device
from iot.service import IOTService, run_parallel, run_sequence


async def main() -> None:
    service = IOTService()

    hue_light = Device("Hue Light")
    speaker = Device("Speaker")
    smart_toilet = Device("Smart Toilet")

    await service.register_devices([hue_light, speaker, smart_toilet])

    # Wake up program:
    # - Light turns on & Speaker turns on/plays music can run in parallel
    # - BUT Speaker must turn on BEFORE playing music!
    await run_parallel(
        hue_light.send_message("switch_on"),
        run_sequence(
            speaker.send_message("switch_on"),
            speaker.send_message("play_music"),
        ),
    )

    # Sleep program:
    # - Light turns off, Speaker turns off, Smart Toilet flush -> clean
    # - Toilet MUST flush BEFORE clean!
    await run_parallel(
        hue_light.send_message("switch_off"),
        speaker.send_message("switch_off"),
        run_sequence(
            smart_toilet.send_message("flush"),
            smart_toilet.send_message("clean"),
        ),
    )

    await service.unregister_devices()


if __name__ == "__main__":
    asyncio.run(main())
