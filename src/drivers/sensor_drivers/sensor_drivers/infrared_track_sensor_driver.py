#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray

from util.Raspbot_Library import Raspbot


class InfraredSensorDriverNode(Node):
    """Publisher Node to read and publish IR Track Sensor Value"""

    def __init__(self):
        super().__init__("infrared_track_sensor_driver")
        # initialize raspbot
        self.raspbot_ = Raspbot()
        # create publisher
        self.publisher_ = self.create_publisher(UInt8MultiArray, "trackline_state", 10)
        self.timer_ = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info(f"InfraredSensorDriverNode initiated")

    def timer_callback(self):
        # read and publish sensor data
        trackline_state = self.raspbot_.Read_IR_Sensor()
        msg = UInt8MultiArray()
        msg.data = trackline_state
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing tracking line status: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = InfraredSensorDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
