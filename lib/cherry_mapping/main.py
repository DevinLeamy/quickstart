from visualizer import PointCloudVisualizer

from lib.messages.point_cloud_msg import POINT_CLOUD_MSG
from lib.messages.topic_to_message_type import (
    TOPIC_POINT_CLOUD,
)
from lib.messages.mqtt_utils import MQTTSubscriber


class DesktopVisualizer:
    def __init__(self, raspberry_pi_ip):
        self.visualizer = PointCloudVisualizer()
        self.mqtt_subscriber = MQTTSubscriber(
            broker_address=raspberry_pi_ip,
            topic_to_message_map={
                TOPIC_POINT_CLOUD: POINT_CLOUD_MSG
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
            TOPIC_POINT_CLOUD)

        print(f"POINT CLOUD MESSAGE: {point_cloud_message}")

        if point_cloud_message is not None:
            self.visualizer.visualize(point_cloud_message.points)

    def close(self):
        self.mqtt_subscriber.stop()
        self.visualizer.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost")
    args = parser.parse_args()

    visualizer = DesktopVisualizer(args.ip)
    visualizer.run()
