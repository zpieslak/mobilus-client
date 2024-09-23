import json
from google.protobuf.json_format import MessageToJson
from mobilus_client.utils.types import MessageResponse


class MessageSerializer:
    @staticmethod
    def serialize_to_json(message: MessageResponse) -> str:
        return MessageToJson(message)

    @staticmethod
    def serialize_list_to_json(messages: list[MessageResponse]) -> str:
        return json.dumps(
            [
                json.loads(
                    MessageSerializer.serialize_to_json(message)
                )
                for message in messages
            ]
        )
