from dataclasses import dataclass
import numpy as np

from lib.messages.mqtt_message_base import MqttMessageBase


class POINT_CLOUD_MSG(MqttMessageBase):
    timestamp: float
    points: np.ndarray  # Nx3 array of points (x,y,z)

    def __init__(self, timestamp: float, points: np.ndarray):
        self.timestamp = timestamp
        self.points = points
