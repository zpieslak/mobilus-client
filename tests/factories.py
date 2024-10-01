from __future__ import annotations

import factory

from mobilus_client.proto import (
    CallEvent,
    CallEventsRequest,
    CurrentStateEvent,
    CurrentStateRequest,
    CurrentStateResponse,
    Device,
    DevicesListRequest,
    DevicesListResponse,
    LoginRequest,
    LoginResponse,
)


class BaseFactory(factory.Factory):  # type: ignore[misc]
    pass


class LoginRequestFactory(BaseFactory):
    class Meta:
        model = LoginRequest

    login = factory.Faker("word")
    password = factory.Faker("binary", length=16)


class LoginResponseFactory(BaseFactory):
    class Meta:
        model = LoginResponse

    login_status = 0
    private_key = factory.Faker("binary", length=16)
    public_key = factory.Faker("binary", length=16)
    admin = factory.Faker("boolean")
    serial_number = factory.Faker("word")
    user_id = factory.Faker("random_int", min=1, max=100)

    class Params:
        failed = factory.Trait(
            login_status=1,
        )


class CurrentStateRequestFactory(BaseFactory):
    class Meta:
        model = CurrentStateRequest


class CurrentStateEventFactory(BaseFactory):
    class Meta:
        model = CurrentStateEvent

    device_id: int = factory.Faker("random_int", min=1, max=100)
    event_number: int = factory.Faker("random_int", min=1, max=100)
    value: str = factory.Faker("word")


class CurrentStateResponseFactory(BaseFactory):
    class Meta:
        model = CurrentStateResponse

    @factory.post_generation  # type: ignore[misc]
    def event(self, _create: bool | None, extracted: dict[str, str | int] | None) -> None:
        event = CurrentStateEventFactory()

        if isinstance(extracted, dict):
            for key, value in extracted.items():
                setattr(event, key, value)

        self.events.append(event)


class DevicesListRequestFactory(BaseFactory):
    class Meta:
        model = DevicesListRequest


class DeviceFactory(BaseFactory):
    class Meta:
        model = Device

    id: int = factory.Faker("random_int", min=1, max=100)
    name: str = factory.Faker("word")
    type: int = factory.Faker("random_int", min=1, max=100)
    icon: int = factory.Faker("random_int", min=1, max=100)
    inserttime: int = factory.Faker("random_int", min=1, max=100)
    favourite: bool = factory.Faker("boolean")


class DevicesListResponseFactory(BaseFactory):
    class Meta:
        model = DevicesListResponse

    @factory.post_generation  # type: ignore[misc]
    def devices(self, _create: bool | None, extracted: dict[str, str | int | bytes] | None) -> None:
        device = DeviceFactory()

        if isinstance(extracted, list):
            for item in extracted:
                for key, value in item.items():
                    setattr(device, key, value)

                self.devices.append(device)


class CallEventFactory(BaseFactory):
    class Meta:
        model = CallEvent

    device_id: int = factory.Faker("random_int", min=1, max=100)
    event_number: int = factory.Faker("random_int", min=1, max=100)
    value: str = factory.Faker("word")
    platform: int = factory.Faker("random_int", min=1, max=100)


class CallEventsRequestFactory(BaseFactory):
    class Meta:
        model = CallEventsRequest

    @factory.post_generation  # type: ignore[misc]
    def event(self, _create: bool | None, extracted: dict[str, str | int] | None) -> None:
        event = CallEventFactory()

        if isinstance(extracted, dict):
            for key, value in extracted.items():
                setattr(event, key, value)

        self.events.append(event)
