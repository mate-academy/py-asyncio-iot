import asyncio
import inspect
import io
import sys
import unittest
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import main
from iot import devices, service
from iot.message import Message, MessageType


class RecordingDevice:
    def __init__(self, name, events):
        self.name = name
        self.events = events

    async def record(self, command, data=""):
        self.events.append(("start", self.name, command, data))
        await asyncio.sleep(0)
        self.events.append(("end", self.name, command, data))

    async def connect(self):
        await self.record("CONNECT")

    async def disconnect(self):
        await self.record("DISCONNECT")

    async def send_message(self, message_type, data=""):
        await self.record(message_type.name, data)


class InterfaceTests(unittest.TestCase):
    def test_device_and_service_operations_are_async(self):
        for device_class in (
            devices.HueLightDevice,
            devices.SmartSpeakerDevice,
            devices.SmartToiletDevice,
            service.Device,
        ):
            for name in ("connect", "disconnect", "send_message"):
                with self.subTest(device=device_class.__name__, method=name):
                    self.assertTrue(
                        inspect.iscoroutinefunction(getattr(device_class, name))
                    )
        for name in (
            "register_device", "unregister_device", "send_msg", "run_program"
        ):
            with self.subTest(service_method=name):
                self.assertTrue(
                    inspect.iscoroutinefunction(getattr(service.IOTService, name))
                )


class AsyncOperationTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_devices_yield_control_while_waiting(self):
        for device_class in (
            devices.HueLightDevice,
            devices.SmartSpeakerDevice,
            devices.SmartToiletDevice,
        ):
            device = device_class()
            for name in ("connect", "disconnect", "send_message"):
                with self.subTest(device=device_class.__name__, method=name):
                    method = getattr(device, name)
                    self.assertTrue(inspect.iscoroutinefunction(method))
                    events = []

                    async def operation():
                        if name == "send_message":
                            await method(MessageType.SWITCH_ON)
                        else:
                            await method()
                        events.append("completed")

                    async def other_task():
                        events.append("other task ran")

                    with patch.object(devices, "TIME_TO_SLEEP", 0.01):
                        with redirect_stdout(io.StringIO()):
                            await asyncio.gather(operation(), other_task())
                    self.assertEqual(events, ["other task ran", "completed"])

    async def test_sequence_waits_for_each_operation(self):
        runner = getattr(service, "run_sequence", None)
        self.assertTrue(callable(runner), "run_sequence must be provided")
        events = []
        device = RecordingDevice("light", events)
        await runner(device.record("first"), device.record("second"))
        self.assertEqual(
            [(event[0], event[2]) for event in events],
            [("start", "first"), ("end", "first"),
             ("start", "second"), ("end", "second")],
        )

    async def test_parallel_overlaps_independent_operations(self):
        runner = getattr(service, "run_parallel", None)
        self.assertTrue(callable(runner), "run_parallel must be provided")
        events = []
        device = RecordingDevice("light", events)
        await runner(device.record("first"), device.record("second"))
        self.assertEqual([event[0] for event in events],
                         ["start", "start", "end", "end"])

    async def test_registration_messages_and_unregistration(self):
        self.assertTrue(inspect.iscoroutinefunction(
            service.IOTService.register_device
        ))
        events = []
        device = RecordingDevice("light", events)
        iot = service.IOTService()
        device_id = await iot.register_device(device)
        self.assertIs(iot.get_device(device_id), device)
        self.assertEqual(events[-1], ("end", "light", "CONNECT", ""))
        await iot.send_msg(Message(device_id, MessageType.CHANGE_COLOR, "blue"))
        self.assertEqual(events[-1], ("end", "light", "CHANGE_COLOR", "blue"))
        await iot.unregister_device(device_id)
        self.assertNotIn(device_id, iot.devices)
        self.assertEqual(events[-1], ("end", "light", "DISCONNECT", ""))

    async def test_run_program_overlaps_independent_messages(self):
        self.assertTrue(inspect.iscoroutinefunction(
            service.IOTService.run_program
        ))
        events = []
        iot = service.IOTService()
        iot.devices = {
            name: RecordingDevice(name, events) for name in ("light", "speaker")
        }
        with redirect_stdout(io.StringIO()):
            await iot.run_program([
                Message("light", MessageType.SWITCH_OFF),
                Message("speaker", MessageType.SWITCH_OFF),
            ])
        self.assertEqual([event[0] for event in events],
                         ["start", "start", "end", "end"])


class ProgramTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.assertTrue(inspect.iscoroutinefunction(main.main))
        self.events = []
        light = RecordingDevice("light", self.events)
        speaker = RecordingDevice("speaker", self.events)
        toilet = RecordingDevice("toilet", self.events)
        with (
            patch.object(main, "HueLightDevice", return_value=light),
            patch.object(main, "SmartSpeakerDevice", return_value=speaker),
            patch.object(main, "SmartToiletDevice", return_value=toilet),
            redirect_stdout(io.StringIO()),
        ):
            await main.main()

    async def test_devices_connect_concurrently(self):
        connection_events = [e[0] for e in self.events if e[2] == "CONNECT"]
        self.assertEqual(connection_events,
                         ["start"] * 3 + ["end"] * 3)
        last_connection = max(i for i, e in enumerate(self.events)
                              if e[2] == "CONNECT")
        first_command = min(i for i, e in enumerate(self.events)
                            if e[2] != "CONNECT")
        self.assertLess(last_connection, first_command)

    async def test_all_commands_keep_their_device_and_data(self):
        commands = Counter(e[1:] for e in self.events
                           if e[0] == "end" and e[2] != "CONNECT")
        self.assertEqual(commands, Counter([
            ("light", "SWITCH_ON", ""),
            ("speaker", "SWITCH_ON", ""),
            ("speaker", "PLAY_SONG", "Rick Astley - Never Gonna Give You Up"),
            ("light", "SWITCH_OFF", ""),
            ("speaker", "SWITCH_OFF", ""),
            ("toilet", "FLUSH", ""),
            ("toilet", "CLEAN", ""),
        ]))

    async def test_speaker_is_on_before_music_starts(self):
        self.assertLess(
            self.events.index(("end", "speaker", "SWITCH_ON", "")),
            self.events.index(("start", "speaker", "PLAY_SONG",
                               "Rick Astley - Never Gonna Give You Up")),
        )

    async def test_toilet_finishes_flushing_before_cleaning(self):
        self.assertLess(
            self.events.index(("end", "toilet", "FLUSH", "")),
            self.events.index(("start", "toilet", "CLEAN", "")),
        )

    async def test_sleep_waits_for_wake_up_and_overlaps_independent_commands(self):
        wake_ends = [i for i, e in enumerate(self.events)
                     if e[0] == "end" and e[2] in ("SWITCH_ON", "PLAY_SONG")]
        sleep_starts = [i for i, e in enumerate(self.events)
                        if e[0] == "start" and e[2] in ("SWITCH_OFF", "FLUSH")]
        sleep_ends = [i for i, e in enumerate(self.events)
                      if e[0] == "end" and e[2] in ("SWITCH_OFF", "FLUSH")]
        self.assertLess(max(wake_ends), min(sleep_starts))
        self.assertLess(max(sleep_starts), min(sleep_ends))
        self.assertLess(
            self.events.index(("start", "light", "SWITCH_ON", "")),
            self.events.index(("end", "speaker", "SWITCH_ON", "")),
        )
        self.assertLess(
            self.events.index(("start", "speaker", "SWITCH_ON", "")),
            self.events.index(("end", "light", "SWITCH_ON", "")),
        )


if __name__ == "__main__":
    unittest.main()
