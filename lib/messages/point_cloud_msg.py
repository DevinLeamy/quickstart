from dataclasses import dataclass
import numpy as np
from typing import Dict, Any

import json

from lib.messages.mqtt_message_base import MqttMessageBase


class POINT_CLOUD_MSG(MqttMessageBase):
    timestamp: float
    points: np.ndarray  # Nx3 array of points (x,y,z)

    def __init__(self, timestamp: float, points: np.ndarray):
        self.timestamp = timestamp
        self.points = points

    def convert_to_playload(self) -> str:
        """Convert message to dictionary for MQTT transmission."""
        try:
            data = {
                'timestamp': self.timestamp,
                'points': self.points.tolist()
            }
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            raise Exception(f'Error converting to payload: {e}') from e

    @classmethod
    def convert_to_message(self, payload):
        """Create message from dictionary received from MQTT."""
        try:
            data = json.loads(payload)
            if 'data' in data:
                data = data['data']
            self.timestamp = data['timestamp']
            self.points = np.array(data['points'])
        except (json.JSONDecodeError, KeyError) as e:
            raise Exception(f'Error converting from payload: {e}') from e
