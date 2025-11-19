#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.srv import SetHeadlights
from util.Raspbot_Library import Raspbot


class HeadlightDriverNode(Node):
    def __init__(self):
        super().__init__("headlight_driver")
        self.raspbot_ = Raspbot()
        self.srv = self.create_service(
            SetHeadlights, "set_headlights", self.set_headlights_callback
        )

    def set_headlights_callback(self, request, response):
        if request.id == 0:
            response.success = self.raspbot_.Ctrl_Headlights_ALL(
                request.r, request.g, request.b
            )
        else:
            response.success = self.raspbot_.Ctrl_Headlights_ID(
                request.id, request.r, request.g, request.b
            )
        self.get_logger().info(
            f"[Set Headlights] Incoming request for Headlight number {request.id} with RGB=({request.r, request.g, request.b})"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = HeadlightDriverNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
