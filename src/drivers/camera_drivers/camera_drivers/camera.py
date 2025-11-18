#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class CameraNode(Node):
    def __init__(self):
        super().__init__("camera")
        self.get_logger().info("Hello World")


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
