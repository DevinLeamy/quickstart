import time
from sshkeyboard import listen_keyboard

from lib.messages.mqtt_utils import MQTTPublisher
from lib.messages.target_velocity_msg import TARGET_VELOCITY_MSG
from lib.messages.topic_to_message_type import TOPIC_TARGET_VELOCITY

from lib.sensors.realsense.realsense_manager import RealSenseManager

# ------------------------------------------------------------------------------------
# Constants & Setup
# ------------------------------------------------------------------------------------
mqtt_publisher = MQTTPublisher(broker_address="localhost", topic_to_message_map={
                               TOPIC_TARGET_VELOCITY: TARGET_VELOCITY_MSG})
mqtt_publisher.run()

class FrameEncoding:
    def __init__(self):
        pass

class LineFollower:
    def __init__(self):
        self.camera = RealSenseManager()
        self.camera.start_pipeline()

        listen_keyboard(
            on_press=self.press,
            on_release=self.release,
        )

    def run(self):
        frame = self.camera.get_color_frame()

        frame_encoding = self.process_frame(frame)
        action = self.generate_action(frame_encoding)
        self.perform_action(action)

    # Generate a frame encoding from a frame.
    def process_frame(self, frame):
        pass

    # Generate an action from a frame encoding.
    def generate_action(self, frame_encoding):
        pass

    # Perform an action.
    def perform_action(self, action):
        pass

    def press(key):
        # Start algorithm.
        if key.lower() == 's':
            mqtt_publisher.publish_msg(
                TOPIC_TARGET_VELOCITY, TARGET_VELOCITY_MSG(time.time(), 0.25, 0.0))
        elif key.lower() == 'e':
            mqtt_publisher.publish_msg(
                TOPIC_TARGET_VELOCITY, TARGET_VELOCITY_MSG(time.time(), 0.0, -10.0))
        else:
            print(f"Pressed key: {key}")

    def release(key):
        print(f"Released key: {key}")
        # Stop motors when key is released
        mqtt_publisher.publish_msg(
            TOPIC_TARGET_VELOCITY, TARGET_VELOCITY_MSG(time.time(), 0.0, 0.0))


if __name__ == "__main__":
    try:
        line_follower = LineFollower()
        line_follower.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mqtt_publisher.publish_msg(
            TOPIC_TARGET_VELOCITY, TARGET_VELOCITY_MSG(time.time(), 0.0, 0.0))
        mqtt_publisher.stop()
        print("Shutdown complete.")
