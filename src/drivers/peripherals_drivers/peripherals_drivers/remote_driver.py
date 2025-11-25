#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from util.Raspbot_Library import Raspbot

SENSOR_HZ = 10


class RemoteDriverNode(Node):
    """Publisher Node to receive and publish Infrared Remote Value"""

    def __init__(self):
        super().__init__("remote_driver")
        # initialize raspbot and turn IR sensor on
        self.raspbot_ = Raspbot()
        self.raspbot_.Ctrl_IR_Remote_Sensor(1)
        # create publisher
        self.publisher_ = self.create_publisher(String, "infrared_remote_value", 10)
        self.timer_ = self.create_timer(1 / SENSOR_HZ, self.timer_callback)
        self.get_logger().info(f"RemoteDriverNode initiated")

    def timer_callback(self):
        # read and publish value
        value = self.raspbot_.Read_IR_Remote_Sensor()
        msg = String()
        msg.data = str(value)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing infrared remote status: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = RemoteDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.raspbot_.Ctrl_IR_Remote_Sensor(0)  # turn off sensor
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
