import factory
from typing import Any, Optional, Dict
from mobilus_client.proto import (
    CallEvent,
    CallEventsRequest,
    CurrentStateRequest,
    CurrentStateResponse,
    CurrentStateEvent,
    Device,
    DevicesListRequest,
    DevicesListResponse,
    LoginResponse,
    LoginRequest
)


class BaseFactory(factory.Factory):  # type: ignore[misc]
    pass


class LoginRequestFactory(BaseFactory):
    class Meta:
        model = LoginRequest

    login = factory.Faker('word')
    password = factory.Faker('binary', length=16)


class LoginResponseFactory(BaseFactory):
    class Meta:
        model = LoginResponse

    login_status = 0
    private_key = factory.Faker('binary', length=16)
    public_key = factory.Faker('binary', length=16)
    admin = factory.Faker('boolean')
    serial_number = factory.Faker('word')
    user_id = factory.Faker('random_int', min=1, max=100)

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

    device_id: int = factory.Faker('random_int', min=1, max=100)
    event_number: int = factory.Faker('random_int', min=1, max=100)
    value: str = factory.Faker('word')


class CurrentStateResponseFactory(BaseFactory):
    class Meta:
        model = CurrentStateResponse

    @factory.post_generation  # type: ignore[misc]
    def event(obj: CurrentStateResponse, create: bool, extracted: Optional[Dict[str, Any]], **kwargs: Any) -> None:
        event = CurrentStateEventFactory()

        if isinstance(extracted, dict):
            for key, value in extracted.items():
                setattr(event, key, value)

        obj.events.append(event)


class DevicesListRequestFactory(BaseFactory):
    class Meta:
        model = DevicesListRequest


class DeviceFactory(BaseFactory):
    class Meta:
        model = Device

    id: int = factory.Faker('random_int', min=1, max=100)
    name: str = factory.Faker('word')
    type: int = factory.Faker('random_int', min=1, max=100)
    icon: int = factory.Faker('random_int', min=1, max=100)
    inserttime: int = factory.Faker('random_int', min=1, max=100)
    favourite: bool = factory.Faker('boolean')


class DevicesListResponseFactory(BaseFactory):
    class Meta:
        model = DevicesListResponse

    @factory.post_generation  # type: ignore[misc]
    def devices(obj: DevicesListResponse, create: bool, extracted: Optional[Dict[str, Any]], **kwargs: Any) -> None:
        device = DeviceFactory()

        if isinstance(extracted, list):
            for item in extracted:
                for key, value in item.items():
                    setattr(device, key, value)

                obj.devices.append(device)


class CallEventFactory(BaseFactory):
    class Meta:
        model = CallEvent

    device_id: int = factory.Faker('random_int', min=1, max=100)
    event_number: int = factory.Faker('random_int', min=1, max=100)
    value: str = factory.Faker('word')
    platform: int = factory.Faker('random_int', min=1, max=100)


class CallEventsRequestFactory(BaseFactory):
    class Meta:
        model = CallEventsRequest

    @factory.post_generation  # type: ignore[misc]
    def event(obj: CallEventsRequest, create: bool, extracted: Optional[Dict[str, Any]], **kwargs: Any) -> None:
        event = CallEventFactory()

        if isinstance(extracted, dict):
            for key, value in extracted.items():
                setattr(event, key, value)

        obj.events.append(event)
