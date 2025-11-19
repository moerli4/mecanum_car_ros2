#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.srv import SetMotor
from util.Raspbot_Library import Raspbot


class MotorDriverNode(Node):
    """Service Node to set Motor Speeds"""
    def __init__(self):
        super().__init__("motor_driver")
        # initialize raspbot
        self.raspbot_ = Raspbot()
        # create service
        self.srv = self.create_service(SetMotor, "set_motor", self.set_motor_callback)

    def set_motor_callback(self, request, response):
        # set motor at given id to given direction and speed
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
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
