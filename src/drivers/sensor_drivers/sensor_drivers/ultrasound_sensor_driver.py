#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt64

from util.Raspbot_Library import Raspbot

SENSOR_HZ = 10


class UltrasoundSensorDriverNode(Node):
    """Publisher Node to read and publish Ultrasound Sensor Value"""

    def __init__(self):
        super().__init__("ultrasound_sensor_driver")
        # initialize raspbot and turn on ultrasound sensor
        self.raspbot_ = Raspbot()
        self.raspbot_.Ctrl_Ultrasound_Sensor(1)
        # create publisher
        self.publisher_ = self.create_publisher(UInt64, "ultrasound_distance", 10)
        self.timer_ = self.create_timer(1 / SENSOR_HZ, self.timer_callback)
        self.get_logger().info(f"UltrasoundSensorDriverNode initiated")

    def timer_callback(self):
        # read and publish sensor data
        ud = self.raspbot_.Read_Ultrasound_Sensor()
        msg = UInt64()
        msg.data = int(ud)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing ultrasound sensor status: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = UltrasoundSensorDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.raspbot_.Ctrl_Ultrasound_Sensor(0)  # turn off sensor
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
