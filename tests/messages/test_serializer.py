import json
import unittest

from mobilus_client.messages.serializer import MessageSerializer
from tests.factories import (
    CallEventsRequestFactory,
    CurrentStateResponseFactory,
    DevicesListResponseFactory,
)


class TestMessageSerializer(unittest.TestCase):
    def test_serialize_device_list_response_to_json(self) -> None:
        request = DevicesListResponseFactory(
            devices=[
                {
                    "id": 1,
                    "name": "device_name",
                    "type": 2,
                    "icon": 3,
                    "inserttime": 4,
                    "favourite": True,
                },
            ],
        )

        result = MessageSerializer.serialize_to_json(request)

        self.assertEqual(json.loads(result), {
            "devices": [
                {
                    "id": "1",
                    "name": "device_name",
                    "type": 2,
                    "icon": 3,
                    "inserttime": "4",
                    "favourite": True,
                },
            ],
        })

    def test_serialize_current_state_response_to_json(self) -> None:
        request = CurrentStateResponseFactory(
            event={
                "device_id": 1,
                "event_number": 7,
                "value": "value",
            },
        )

        result = MessageSerializer.serialize_to_json(request)

        self.assertEqual(json.loads(result), {
            "events": [
                {
                    "deviceId": "1",
                    "eventNumber": 7,
                    "value": "value",
                },
            ],
        })

    def test_serialize_call_events_request_to_json(self) -> None:
        request = CallEventsRequestFactory(
            event={
                "device_id": 1,
                "event_number": 7,
                "value": "value",
                "platform": 1,
            },
        )

        result = MessageSerializer.serialize_to_json(request)

        self.assertEqual(json.loads(result), {
            "events": [
                {
                    "deviceId": "1",
                    "eventNumber": 7,
                    "value": "value",
                    "platform": 1,
                },
            ],
        })

    def test_serialize_call_events_request_list_to_json(self) -> None:
        request1 = CallEventsRequestFactory(
            event={
                "device_id": 1,
                "event_number": 7,
                "value": "value",
                "platform": 1,
            },
        )
        request2 = CallEventsRequestFactory(
            event={
                "device_id": 2,
                "event_number": 8,
                "value": "value2",
                "platform": 2,
            },
        )

        result = MessageSerializer.serialize_list_to_json([request1, request2])

        self.assertEqual(json.loads(result), [
            {
                "events": [
                    {
                        "deviceId": "1",
                        "eventNumber": 7,
                        "value": "value",
                        "platform": 1,
                    },
                ],
            },
            {
                "events": [
                    {
                        "deviceId": "2",
                        "eventNumber": 8,
                        "value": "value2",
                        "platform": 2,
                    },
                ],
            },
        ])
