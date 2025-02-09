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

SPEED = 0.25  # meters per second


class FrameEncoding:
    def __init__(self, value: float | None = None):
        # Value between 0 and 1.
        # 0.5 is the middle.
        # None if no line is detected.
        self.value = value


class Action:
    def __init__(self, linear_velocity: float, angular_velocity: float):
        self.linear_velocity = linear_velocity
        self.angular_velocity = angular_velocity


class LineFollower:
    def __init__(self):
        self.camera = RealSenseManager()
        self.camera.start_pipeline()
        self.started = False

        listen_keyboard(
            on_press=self.press,
            on_release=self.release,
        )

    def run(self):
        while True:
            if not self.started:
                time.sleep(0.1)
                continue

            frame = self.camera.get_color_frame()

            frame_encoding = self.process_frame(frame)
            action = self.generate_action(frame_encoding)
            self.perform_action(action)

            time.sleep(0.1)

    # Generate a frame encoding from a frame.
    def process_frame(self, frame):
        pass

    # Generate an action from a frame encoding.
    def generate_action(self, frame_encoding: FrameEncoding) -> Action:
        if frame_encoding.value is None:
            return Action(0.0, 0.0)

        # Convert frame encoding to steering action
        # frame_encoding.value of 0.5 means straight ahead
        # < 0.5 means line is to the left, > 0.5 means line is to the right
        error = frame_encoding.value - 0.5

        # Scale the angular velocity based on the error
        # Negative angular velocity turns left, positive turns right
        angular_velocity = -error * 20.0  # Adjust multiplier as needed

        return Action(SPEED, angular_velocity)

    # Perform an action.
    def perform_action(self, action: Action):
        mqtt_publisher.publish_msg(
            TOPIC_TARGET_VELOCITY,
            TARGET_VELOCITY_MSG(
                time.time(),
                action.linear_velocity,
                action.angular_velocity
            )
        )

    def press(self, key):
        if key.lower() == 's':
            self.started = True
            self.stop()
        elif key.lower() == 'e':
            self.started = False
            self.stop()
        else:
            print(f"Pressed key: {key}")

    def stop(self, key):
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
