#!/usr/bin/env python3
import rclpy
from car_interfaces_pkg.srv import ControlServo
from rclpy.node import Node

from util.Raspbot_Library import Raspbot


class ServoControlNode(Node):
    """Service Node to control the angle of the camera servos"""

    def __init__(self):
        super().__init__("servo_control")
        self.raspbot_ = Raspbot()
        self.srv = self.create_service(
            ControlServo, "ctrl_servo", self.ctrl_servo_callback
        )

    def ctrl_servo_callback(self, request, response):
        response.success = self.raspbot_.Ctrl_Camera_Servo(
            request.id, request.set_angle
        )
        self.get_logger().info(
            f"[Servo Control] Incoming request {request.id, request.set_angle}"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    servo_control = ServoControlNode()
    rclpy.spin(servo_control)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
