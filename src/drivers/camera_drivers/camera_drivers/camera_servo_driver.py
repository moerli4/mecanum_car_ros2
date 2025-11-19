#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.srv import SetServo
from util.Raspbot_Library import Raspbot


class ServoDriverServo(Node):
    """Service Node to control the angle of the camera servos"""

    def __init__(self):
        super().__init__("camera_servo_driver")
        self.raspbot_ = Raspbot()
        self.srv = self.create_service(SetServo, "ctrl_servo", self.ctrl_servo_callback)

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
    servo_drivers = ServoDriverServo()
    rclpy.spin(servo_drivers)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
