import open3d as o3d
import numpy as np

from visualizer import PointCloudVisualizer
from wv_manager import DepthWavemapManager

from lib.messages.wavemap_occupied_points_msg import WAVEMAP_OCCUPIED_POINTS_MSG
from lib.messages.topic_to_message_type import (
    TOPIC_WAVEMAP_OCCUPIED_POINTS,
)
from lib.messages.mqtt_utils import MQTTSubscriber


class Visualizer:
    def __init__(self):
        self.visualizer = PointCloudVisualizer()
        self.mqtt_subscriber = MQTTSubscriber(
            broker_address="localhost",
            topic_to_message_map={
                TOPIC_WAVEMAP_OCCUPIED_POINTS: WAVEMAP_OCCUPIED_POINTS_MSG,
            }
        )

    def run(self):
        self.mqtt_subscriber.start()

        try:
            while True:
                self.process_input()
        except KeyboardInterrupt:
            self.close()

    def process_input(self):
        point_cloud_message = self.mqtt_subscriber.get_latest_message(
            TOPIC_WAVEMAP_OCCUPIED_POINTS)

        print(f"POINT CLOUD MESSAGE: {point_cloud_message}")

    def close(self):
        self.mqtt_subscriber.stop()
        self.visualizer.close()


visualizer = Visualizer()
visualizer.run()
