import time
from sshkeyboard import listen_keyboard

from lib.messages.mqtt_utils import MQTTPublisher
from lib.messages.target_velocity_msg import TARGET_VELOCITY_MSG
from lib.messages.topic_to_message_type import TOPIC_TARGET_VELOCITY

from lib.sensors.realsense.realsense_manager import RealSenseManager

import cv2
import numpy as np

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

        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define yellow color range in HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create mask for yellow pixels
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour (assuming it's the line)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Calculate centroid of the largest contour
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return {"centroid": (cx, cy), "frame_width": frame.shape[1]}
        
        # Return None if no yellow line is detected
        return None

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
