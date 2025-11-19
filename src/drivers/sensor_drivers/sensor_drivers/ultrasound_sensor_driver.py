#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt64

from util.Raspbot_Library import Raspbot


class UltrasoundSensorDriverNode(Node):
    def __init__(self):
        super().__init__("ultrasound_sensor_driver")
        self.raspbot_ = Raspbot()
        self.raspbot_.Ctrl_Ultrasound_Sensor(1)
        self.publisher_ = self.create_publisher(UInt64, "ultrasound_distance", 10)
        self.timer_ = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        ud = self.raspbot_.Read_Ultrasound_Sensor()
        msg = UInt64()
        msg.data = int(ud)
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = UltrasoundSensorDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.raspbot_.Ctrl_Ultrasound_Sensor(0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
