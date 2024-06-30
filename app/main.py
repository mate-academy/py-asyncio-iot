import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import MessageType, Message
from iot.service import IOTService


class IOTInterface:
    def __init__(self, service: IOTService):
        self.service = service
        self.devices = {}

    async def register_devices(self):
        hue_light = HueLightDevice()
        speaker = SmartSpeakerDevice()
        toilet = SmartToiletDevice()

        start = time.perf_counter()

        devices_ids = await asyncio.gather(
            self.service.register_device(hue_light),
            self.service.register_device(speaker),
            self.service.register_device(toilet),
        )

        self.devices = {
            "hue_light": devices_ids[0],
            "speaker": devices_ids[1],
            "toilet": devices_ids[2],
        }

        print("Devices has been registered!")

        end = time.perf_counter()

        print("\nElapsed:", end - start)


    async def run_wake_up_program(self):
        program = [
            Message(self.devices["hue_light"], MessageType.SWITCH_ON, "Run"),
            Message(self.devices["speaker"], MessageType.SWITCH_ON, "Run"),
            Message(
                self.devices["speaker"],
                MessageType.PLAY_SONG, "Rammstein - Du hast"
            ),
            Message(self.devices["toilet"], MessageType.OPEN, "Run"),
        ]

        start = time.perf_counter()
        await self.service.run_program(program)
        end = time.perf_counter()

        print("\nElapsed:", end - start)

    async def run_sleep_program(self):
        program = [
            Message(
                self.devices["hue_light"],MessageType.SWITCH_OFF, "Stop"
            ),
            Message(self.devices["speaker"], MessageType.SWITCH_OFF, "Stop"),
            Message(self.devices["toilet"], MessageType.FLUSH, "Stop"),
            Message(self.devices["toilet"], MessageType.CLEAN, "Stop"),
            Message(self.devices["toilet"], MessageType.CLOSE, "Done"),
        ]

        start = time.perf_counter()
        await self.service.run_program(program)
        end = time.perf_counter()

        print("\nElapsed:", end - start)

    async def get_menu(self):
        while True:
            print("\n====== Custom IOT Menu ======")
            print("1. Register Devices")
            print("2. Run Wake Up Program")
            print("3. Run Sleep Program")
            print("4. Exit")

            number = input("Enter your choice: ")

            if number == "1":
                await self.register_devices()
            elif number == "2":
                if not self.devices:
                    print("Please register devices first.")
                else:
                    await self.run_wake_up_program()
            elif number == "3":
                if not self.devices:
                    print("Please register devices first.")
                else:
                    await self.run_sleep_program()
            elif number == "4":
                break
            else:
                print("Invalid choice. Please try again.")


async def main() -> None:
    service = IOTService()
    interface = IOTInterface(service)
    await interface.get_menu()


if __name__ == "__main__":
    start = time.perf_counter()
    print("Start the connections...\n")
    asyncio.run(main())
    end = time.perf_counter()
    result = end - start

    print(f"The program ran for: {result} seconds")
