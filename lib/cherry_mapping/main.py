from visualizer import PointCloudVisualizer
import paho.mqtt.client as mqtt
import json
from lib.messages.point_cloud_msg import POINT_CLOUD_MSG
from lib.messages.topic_to_message_type import TOPIC_POINT_CLOUD
import numpy as np


class DesktopVisualizer:
    def __init__(self, raspberry_pi_ip):
        self.visualizer = PointCloudVisualizer()

        # Setup MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print(f"Connecting to broker at {raspberry_pi_ip}...")
        self.client.connect(raspberry_pi_ip, 1883)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(TOPIC_POINT_CLOUD)
        print(f"Subscribed to {TOPIC_POINT_CLOUD}")

    def on_message(self, client, userdata, message: mqtt.MQTTMessage):
        try:
            message = json.loads(message.payload.decode())
            points = message['points']
            array = np.array(points)
            print(f"Received payload: {len(array)}")
            self.visualizer.visualize(array)
        except Exception as e:
            print(f"Error processing message: {e}")

    def run(self):
        try:
            print("Listening for point cloud messages...")
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.close()

    def close(self):
        self.client.disconnect()
        self.visualizer.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost",
                        help="IP address of the Raspberry Pi (first address from hostname -I)")
    args = parser.parse_args()

    visualizer = DesktopVisualizer(args.ip)
    visualizer.run()
