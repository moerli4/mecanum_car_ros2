#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from driver_interfaces.srv import SetAllMotors, SetMotor
from util.Raspbot_Library import Raspbot


class MotorDriverNode(Node):
    """Service Node to set Motor Speeds"""

    def __init__(self):
        super().__init__("motor_driver")
        # initialize raspbot
        self.raspbot_ = Raspbot()
        # create service
        self.srv = self.create_service(SetMotor, "set_motor", self.set_motor_callback)
        self.srv_all = self.create_service(
            SetAllMotors, "set_all_motors", self.set_all_motors_callback
        )
        self.get_logger().info(f"MotorDriverNode initiated")

    def set_motor_callback(self, request, response):
        self.get_logger().info(
            f"[Set Motor] Incoming request {request.id, request.dir, request.speed}"
        )
        # set motor at given id to given direction and speed
        response.success = self.raspbot_.Ctrl_Car(
            request.id, request.dir, request.speed
        )
        return response

    def set_all_motors_callback(self, request, response):
        self.get_logger().info(
            f"[Set Motor] Incoming request {request.dir, request.speed}"
        )
        # set motors to given direction and speed
        response.success = 0
        for i, (direction, speed) in enumerate(zip(request.dir, request.speed)):
            direction = int(direction)
            speed = int(speed)
            success = self.raspbot_.Ctrl_Car(i, direction, speed)
            if success != 0:
                response.success = 1
                break  # break if one fails
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
