#!/usr/bin/env python3
import time

import numpy as np
import rclpy
from rclpy.node import Node

from interfaces.srv import SetAllMotors


class MotionController():
    """Motion Controller"""

    def __init__(self, node=Node):
        # dont create node here
        self.node = node

        # create client to drivers
        self.set_all_motors_client_ = self.node.create_client(SetAllMotors, "set_all_motors")

        # info
        self.node.get_logger().info(f"motion control node initialized")

    def set_speed(self, speed: list):
        """set custom speed values for each motor

        Args:
            speed (list): list of length four, speed for each motor as an int of range 0-255
        """
        # get target speeds
        target_speed = np.array(speed)
        
        # send request
        req = SetAllMotors.Request()
        req.speed = abs(target_speed)
        req.dir = (target_speed >= 0).astype(int)
        future = self.set_all_motors_client_.call_async(req)
        
        return future
    
    def forward(self, speed: int):
        """go forward

        Args:
            speed (int): speed, 0-255
        """
        target_speed = np.array(
            [
                speed,
            ]
            * 4
        )

        return self.set_speed(target_speed)

    def backward(self, speed: int):
        """go backward

        Args:
            speed (int): speed, 0-255
        """
        target_speed = np.array(
            [
                -speed,
            ]
            * 4
        )
        return self.set_speed(target_speed)

    def stop(self):
        """stop all motion"""
        target_speed = np.array(
            [
                0,
            ]
            * 4
        )
        return self.set_speed(target_speed)

    def directional_motion(self, direction_angle: int, speed: int):
        """go in the direction of the angle passed

        Args:
            direction_angle (int): direction angle in deg, 0-360
            speed (int): speed, 0-255
        """
        # Convert angle to radians for trigonometric functions
        rad_angle = np.deg2rad(direction_angle)

        # Calculate the speed for each wheel based on the mecanum wheel configuration
        normalization_factor = abs((np.sin(rad_angle) + np.cos(rad_angle))) if (np.sin(rad_angle) + np.cos(rad_angle)) != 0 else 1
        front_left_speed = (np.sin(rad_angle) + np.cos(rad_angle)) / normalization_factor * speed * 255
        rear_left_speed = (-np.cos(rad_angle) + np.sin(rad_angle)) / normalization_factor * speed * 255
        front_right_speed = (-np.cos(rad_angle) + np.sin(rad_angle)) / normalization_factor * speed * 255
        rear_right_speed = (np.sin(rad_angle) + np.cos(rad_angle)) / normalization_factor * speed * 255

        target_speed = [front_left_speed,rear_left_speed,front_right_speed,rear_right_speed]

        return self.set_speed(target_speed)

    def rotate(self, direction: int, speed: int):
        """rotate the car in the specified direction at specified speed

        Args:
            direction (int): direction, [-1,1]
            speed (int): speed at which to rotate, 0-255
        """
        target_speed = np.array([
            direction*speed,direction*speed,-direction*speed,-direction*speed
        ])

        return self.set_speed(target_speed)


def main(args=None):
    # init
    rclpy.init(args=args)

    # initialize demo and create motion controller
    node = rclpy.create_node('motion_controller_demo')
    motion_controller = MotionController(node)

    # short demo
    try:
        # forwards
        motion_controller.forward(30)
        time.sleep(1)

        # stop
        motion_controller.stop()
        time.sleep(1)

        # backwards
        motion_controller.backward(30)
        time.sleep(1)
        
        # stop
        motion_controller.stop()
        time.sleep(1)

        # rotate
        motion_controller.rotate(1,30)
        time.sleep(1)

        # stop
        motion_controller.stop()
        time.sleep(1)

        # go sideways
        motion_controller.directional_motion(90,30)
        time.sleep(1)

        # stop
        motion_controller.stop()
        time.sleep(1)

    finally:
        # shutdown safely
        motion_controller.stop()
        time.sleep(1)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()