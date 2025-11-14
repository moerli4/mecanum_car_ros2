#!/usr/bin/env python3
from car_interfaces_pkg.srv import ControlServo
from util.Raspbot_Library import Raspbot

import rclpy
from rclpy.node import Node


class ServoControlNode(Node):
    def __init__(self):
        super().__init__("servo_control_service")
        self.raspbot_ = Raspbot()
        self.srv = self.create_service(ControlServo, 'ctrl_servo', ctrl_servo_callback)

    def ctrl_servo_callback(self, request, response):
        response.get_angle = self.raspbot_.Ctrl_Camera_Servo(request.id, request.set_angle)
        self.get_logger().info(f"Incoming request {request.id, request.set_angle}")

        return response

def main(args=None):
    rclpy.init(args=args)

    servo_control = ServoControlNode()

    rclpy.spin(servo_control)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()
