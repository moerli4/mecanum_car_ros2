#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from util.Raspbot_Library import Raspbot
from std_msgs.msg import UInt8MultiArray


class InfraredSensorNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("infrared_track_sensor") # MODIFY NAME
        self.raspbot_ = Raspbot()
        self.publisher_ = self.create_publisher(UInt8MultiArray, "trackline_state", 10)
        self.timer_ = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        trackline_state = self.raspbot_.Read_IR_Sensor()
        msg = UInt8MultiArray()
        msg.data = trackline_state
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing tracking line status: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = InfraredSensorNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
