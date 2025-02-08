"""Auto-generated MQTT message class from TOML configuration config/bot_quickstart_msgs.toml."""

import json

from lib.messages.mqtt_message_base import MqttMessageBase


class POINT_CLOUD_MSG(MqttMessageBase):
    """MQTT message class for POINT_CLOUD."""

    timestamp: float = None
    points: list = None

    def __init__(self, timestamp: float | None = None, points: list | None = None):
        """Initialize the message class with given fields."""
        self.timestamp = timestamp
        self.points = points

    def convert_to_payload(self) -> str:
        """Convert the message fields to a JSON payload."""
        try:
            data = {
                'timestamp': self.timestamp,
                'points': self.points,
            }
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            raise Exception(f'Error converting to payload: {e}') from e

    def convert_to_message(self, payload):
        """Convert a JSON payload to message fields."""
        try:
            data = json.loads(payload)
            if 'data' in data:
                data = data['data']
            self.timestamp = data['timestamp']
            self.points = data['points']
        except (json.JSONDecodeError, KeyError) as e:
            raise Exception(f'Error converting from payload: {e}') from e
