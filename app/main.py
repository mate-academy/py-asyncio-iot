import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    # Parallel device registration
    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet),
    )

    # Programme implementation
    await service.run_wake_up_program(hue_light_id, speaker_id)
    await service.run_sleep_program(hue_light_id, speaker_id, toilet_id)

if __name__ == "__main__":
    start = asyncio.run(main())
