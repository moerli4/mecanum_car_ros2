#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.srv import SetServo
from util.Raspbot_Library import Raspbot


class CameraServoDriverNode(Node):
    """Service Node to control the angle of the camera servos"""

    def __init__(self):
        super().__init__("camera_servo_driver")
        # initialize raspbot object
        self.raspbot_ = Raspbot()
        # create service
        self.srv = self.create_service(
            SetServo, "set_camera_servo", self.set_servo_callback
        )
        self.get_logger().info("CameraServoDriverNode initiated")

    def set_servo_callback(self, request, response):
        # set servo angles
        response.success = self.raspbot_.Ctrl_Camera_Servo(
            request.id, request.set_angle
        )
        self.get_logger().info(f"Incoming request {request.id, request.set_angle}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = CameraServoDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
