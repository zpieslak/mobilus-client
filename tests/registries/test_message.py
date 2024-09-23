import unittest
from mobilus_client.registries.message import MessageRegistry
from tests.factories import (
    CallEventsRequestFactory,
    CurrentStateRequestFactory,
    CurrentStateResponseFactory,
    DevicesListRequestFactory,
    DevicesListResponseFactory,
)


class TestMessageRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = MessageRegistry()

    def test_get_requests(self) -> None:
        devices_list_request = DevicesListRequestFactory()
        self.registry.register_request(devices_list_request)

        result = self.registry.get_requests()

        self.assertEqual(result, [devices_list_request])

    def test_get_requests_when_empty(self) -> None:
        result = self.registry.get_requests()

        self.assertEqual(result, [])

    def test_get_responses(self) -> None:
        devices_list_response = DevicesListResponseFactory()
        self.registry.register_response(devices_list_response)

        result = self.registry.get_responses()

        self.assertEqual(result, [devices_list_response])

    def test_get_responses_when_empty(self) -> None:
        result = self.registry.get_responses()

        self.assertEqual(result, [])

    def test_all_responses_received_when_responses_matches_requests(self) -> None:
        call_events_request = CallEventsRequestFactory()
        current_state_request = CurrentStateRequestFactory()
        current_state_response = CurrentStateResponseFactory()
        devices_list_request = DevicesListRequestFactory()
        devices_list_response = DevicesListResponseFactory()
        self.registry.register_request(call_events_request)
        self.registry.register_request(current_state_request)
        self.registry.register_request(devices_list_request)
        self.registry.register_response(call_events_request)
        self.registry.register_response(current_state_response)
        self.registry.register_response(devices_list_response)

        result = self.registry.all_responses_received()

        self.assertTrue(result)

    def test_all_responses_received_when_responses_does_not_match_requests(self) -> None:
        call_events_request = CallEventsRequestFactory()
        current_state_request = CurrentStateRequestFactory()
        self.registry.register_request(call_events_request)
        self.registry.register_request(current_state_request)
        self.registry.register_response(call_events_request)

        result = self.registry.all_responses_received()

        self.assertFalse(result)

    def test_all_responses_received_when_no_requests(self) -> None:
        result = self.registry.all_responses_received()

        self.assertTrue(result)
