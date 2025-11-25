#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.srv import SetHeadlights
from util.Raspbot_Library import Raspbot


class HeadlightDriverNode(Node):
    """Service Node to change color and brightness of headlight strip LEDs"""

    def __init__(self):
        super().__init__("headlight_driver")
        # initialize raspbot
        self.raspbot_ = Raspbot()
        # create service
        self.srv = self.create_service(
            SetHeadlights, "set_headlights", self.set_headlights_callback
        )
        self.get_logger().info(f"HeadlightDriverNode initiated")

    def set_headlights_callback(self, request, response):
        # set headlight colors
        if request.id == 0:  # set all if id = 0
            response.success = self.raspbot_.Ctrl_Headlights_ALL(
                request.r, request.g, request.b
            )
        else:
            response.success = self.raspbot_.Ctrl_Headlights_ID(
                request.id, request.r, request.g, request.b
            )
        self.get_logger().info(
            f"Incoming request for Headlight number {request.id} with RGB=({request.r, request.g, request.b})"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = HeadlightDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
