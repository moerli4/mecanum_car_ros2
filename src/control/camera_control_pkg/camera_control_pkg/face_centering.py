#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from control_interfaces.msg import FaceBoundingBoxArray
from driver_interfaces.srv import SetServo
import numpy as np
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy


class FaceCenteringController(Node):
    """Node to center detected faces using camera servos"""
    
    def __init__(self):
        super().__init__("face_centering_controller")

        # Use reliable qos profile
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Subscribe to face detection results
        self.face_subscriber = self.create_subscription(
            FaceBoundingBoxArray,
            "/mediapipe/face_detection_bboxes",
            self.face_callback,
            qos_profile,
        )

        # Create a service client for setting the servo
        self.servo_client = self.create_client(SetServo, "set_camera_servo")
        self.logger = self.get_logger()
        
        # Ensure the server is available before making requests
        while not self.servo_client.wait_for_service(timeout_sec=1.0):
            self.logger.info("Waiting for Servo service to be available...")
        
    def face_callback(self, msg: FaceBoundingBoxArray):
        # if any faces are detected
        if msg.faces:
            # assume we want to center on the first detected face
            face = msg.faces[0]

            # Calculate the center of the face box for x
            face_center_x = (face.x1 + face.x2) / 2
            position_error_x = (face_center_x - 1 / 2)

            # Calculate the center of the face box for y
            face_center_y = (face.y1 + face.y2) / 2
            frame_width = 1.0  # Assuming the width is normalized between 0 to 1
            position_error_y = (face_center_y - 1 / 2)

            self.control_servo(position_error_x,position_error_y)

    def control_servo(self, position_error_x,position_error_y):
        # Define a simple proportional control for the servo
        angle_adjustment_x, angle_adjustment_y = self.calculate_angle_adjustment(position_error_x,position_error_y)
        
        # send x request
        request = SetServo.Request()
        request.id = 0
        request.set_angle = angle_adjustment_x        

        # Call the service to set servo angle
        self.send_servo_command(request)

        # send y request
        request = SetServo.Request()
        request.id = 1
        request.set_angle = angle_adjustment_y
    
        # Call the service to set servo angle
        self.send_servo_command(request)

    def calculate_angle_adjustment(self, position_error_x,position_error_y):
        # Define a proportional gain
        Kp_x = 30
        angle_adjustment_x = Kp_x * position_error_x + 90 # Scale the error to an angle
        Kp_y = 30
        angle_adjustment_y = Kp_y * position_error_y + 50  # Scale the error to an angle
        return np.clip(angle_adjustment_x, 0, 180),np.clip(angle_adjustment_y, 0, 100)

    def send_servo_command(self, request):
        self.logger.info(f"Sending servo command: id={request.id}, angle={request.set_angle}")
        future = self.servo_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.logger.info("Servo command executed successfully.")
        else:
            self.logger.error("Failed to execute servo command.")


def main(args=None):
    rclpy.init(args=args)
    node = FaceCenteringController()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
