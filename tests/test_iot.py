import asyncio
import contextlib
import io
import unittest
from unittest.mock import AsyncMock, patch

import main
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService, run_parallel, run_sequence


class AsyncIOTTests(unittest.IsolatedAsyncioTestCase):
    async def test_devices_await_nonblocking_io(self):
        for device_type in (HueLightDevice, SmartSpeakerDevice, SmartToiletDevice):
            with self.subTest(device=device_type.__name__):
                device = device_type()
                with (
                    patch("iot.devices.asyncio.sleep", new_callable=AsyncMock) as sleep,
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    await device.connect()
                    await device.send_message(MessageType.SWITCH_ON)
                    await device.disconnect()
                self.assertEqual(sleep.await_count, 3)
                sleep.assert_awaited_with(0.5)

    async def test_registration_and_unregistration_wait_for_device(self):
        service = IOTService()
        device = AsyncMock()

        async def check_connect():
            self.assertEqual(service.devices, {})

        device.connect.side_effect = check_connect
        device_id = await service.register_device(device)
        self.assertIs(service.get_device(device_id), device)

        async def check_disconnect():
            self.assertIn(device_id, service.devices)

        device.disconnect.side_effect = check_disconnect
        await service.unregister_device(device_id)
        self.assertEqual(service.devices, {})
        device.connect.assert_awaited_once()
        device.disconnect.assert_awaited_once()

    async def test_service_forwards_message_and_keeps_program_order(self):
        service = IOTService()
        device = AsyncMock()
        service.devices["speaker"] = device
        messages = [
            Message("speaker", MessageType.SWITCH_ON),
            Message("speaker", MessageType.PLAY_SONG, "song"),
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            await service.run_program(messages)
        self.assertEqual(
            device.send_message.await_args_list,
            [unittest.mock.call(MessageType.SWITCH_ON, ""),
             unittest.mock.call(MessageType.PLAY_SONG, "song")],
        )

    async def test_parallel_operations_overlap_without_timing_assumptions(self):
        started = set()
        both_started = asyncio.Event()

        async def operation(name):
            started.add(name)
            if len(started) == 2:
                both_started.set()
            await both_started.wait()

        await asyncio.wait_for(
            run_parallel(operation("first"), operation("second")), timeout=1,
        )
        self.assertEqual(started, {"first", "second"})

    async def test_sequence_waits_for_completion(self):
        events = []

        async def operation(name):
            events.append((name, "start"))
            await asyncio.sleep(0)
            events.append((name, "end"))

        await run_sequence(operation("first"), operation("second"))
        self.assertEqual(events, [
            ("first", "start"), ("first", "end"),
            ("second", "start"), ("second", "end"),
        ])

    async def test_main_overlaps_independent_work_and_preserves_dependencies(self):
        events = []
        connecting = set()
        all_connecting = asyncio.Event()
        service = IOTService()

        async def connect(device):
            connecting.add(device)
            if len(connecting) == 3:
                all_connecting.set()
            await all_connecting.wait()

        def make_device(name):
            device = AsyncMock()

            async def connect_device():
                await connect(name)

            async def send(message_type, data):
                events.append((name, message_type, "start", data))
                await asyncio.sleep(0)
                events.append((name, message_type, "end", data))

            device.connect.side_effect = connect_device
            device.send_message.side_effect = send
            return device

        with (
            patch.object(main, "IOTService", return_value=service),
            patch.object(main, "HueLightDevice", return_value=make_device("light")),
            patch.object(main, "SmartSpeakerDevice", return_value=make_device("speaker")),
            patch.object(main, "SmartToiletDevice", return_value=make_device("toilet")),
        ):
            await asyncio.wait_for(main.main(), timeout=1)

        def position(name, kind, phase):
            return next(index for index, event in enumerate(events)
                        if event[:3] == (name, kind, phase))

        self.assertEqual(len(events), 14)  # Each of the seven commands starts/ends.
        self.assertLess(position("speaker", MessageType.SWITCH_ON, "end"),
                        position("speaker", MessageType.PLAY_SONG, "start"))
        self.assertLess(position("toilet", MessageType.FLUSH, "end"),
                        position("toilet", MessageType.CLEAN, "start"))
        wake_end = max(position(name, kind, "end") for name, kind in [
            ("light", MessageType.SWITCH_ON),
            ("speaker", MessageType.SWITCH_ON),
            ("speaker", MessageType.PLAY_SONG),
        ])
        for name, kind in [("light", MessageType.SWITCH_OFF),
                           ("speaker", MessageType.SWITCH_OFF),
                           ("toilet", MessageType.FLUSH)]:
            self.assertGreater(position(name, kind, "start"), wake_end)
        self.assertLess(position("speaker", MessageType.SWITCH_ON, "start"),
                        position("light", MessageType.SWITCH_ON, "end"))
        self.assertLess(position("toilet", MessageType.FLUSH, "start"),
                        position("speaker", MessageType.SWITCH_OFF, "end"))
        song_events = [event for event in events if event[1] == MessageType.PLAY_SONG]
        self.assertEqual(song_events[0][3], "Rick Astley - Never Gonna Give You Up")


if __name__ == "__main__":
    unittest.main()
