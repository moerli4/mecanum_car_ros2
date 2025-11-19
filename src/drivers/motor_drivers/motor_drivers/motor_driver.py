#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class MotorDriverNode(Node):
    def __init__(self):
        super().__init__("motor_driver")


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
