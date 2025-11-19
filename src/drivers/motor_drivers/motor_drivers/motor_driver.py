#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.srv import SetMotor
from util.Raspbot_Library import Raspbot


class MotorDriverNode(Node):
    def __init__(self):
        super().__init__("motor_driver")
        self.raspbot_ = Raspbot()
        self.srv = self.create_service(SetMotor, "set_motor", self.set_motor_callback)

    def set_motor_callback(self, request, response):
        response.success = self.raspbot_.Ctrl_Car(
            request.id, request.dir, request.speed
        )
        self.get_logger().info(
            f"[Set Motor] Incoming request {request.id, request.dir, request.speed}"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
