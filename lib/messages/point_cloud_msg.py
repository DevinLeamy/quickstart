from dataclasses import dataclass
import numpy as np
from typing import Dict, Any

from lib.messages.mqtt_message_base import MqttMessageBase


@dataclass
class POINT_CLOUD_MSG(MqttMessageBase):
    timestamp: float
    points: np.ndarray  # Nx3 array of points (x,y,z)

    default_msg_dict = {
        'timestamp': 0.0,
        'points': np.zeros((0, 3))  # Empty Nx3 array
    }

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for MQTT transmission."""
        return {
            'timestamp': self.timestamp,
            'points': self.points.tolist()  # Convert numpy array to list for JSON serialization
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'POINT_CLOUD_MSG':
        """Create message from dictionary received from MQTT."""
        return cls(
            timestamp=float(data['timestamp']),
            points=np.array(data['points'])  # Convert list back to numpy array
        )

    def __init__(self, timestamp: float, points: np.ndarray):
        self.timestamp = timestamp
        self.points = points
