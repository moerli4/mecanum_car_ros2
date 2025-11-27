#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time

from interfaces.srv import SetAllMotors
from std_msgs.msg import Float32MultiArray
import numpy as np

class MotionControlNode(Node):
    """Node for Motion Control"""

    def __init__(self):
        super().__init__("motion_control_node")

        # create client to drivers
        self.set_all_motors_client_ = self.create_client(SetAllMotors, "set_all_motors")

        # speed values
        self.current_speeds = np.array([0, 0, 0, 0])
        self.target_speeds  = np.array([0, 0, 0, 0])

        # update motor values at given frequency with given step increment
        self.motor_update_Hz = 1
        self.motor_update_step = 5
        self.send_request_timer = self.create_timer(1/self.motor_update_Hz, self.update_motor_speeds)

        # create publisher for current states
        self.state_pub_ = self.create_publisher(Float32MultiArray, 'motor_states', 10)

        # info
        self.get_logger().info(f"motion control node initialized")

    def update_motor_speeds(self):
        """incrementally reach the requested target speed
        """

        # do one incremental step towards the target speeds
        if (self.current_speeds != self.target_speeds).any():
            # get next increment
            increment = np.sign(self.target_speeds - self.current_speeds) * self.motor_update_step
            
            # calculate next current speeds
            next_current_speeds = self.current_speeds + increment
            
            # Clamp the overshoot for positive increments
            positive_mask = (increment > 0) & (next_current_speeds > self.target_speeds)
            next_current_speeds[positive_mask] = self.target_speeds[positive_mask]

            # Clamp the overshoot for negative increments
            negative_mask = (increment < 0) & (next_current_speeds < self.target_speeds)
            next_current_speeds[negative_mask] = self.target_speeds[negative_mask]

            # Apply new speeds to motors
            self.current_speeds = next_current_speeds

            # send request
            req = SetAllMotors.Request()
            req.speed = abs(self.current_speeds).tolist()
            req.dir = (self.current_speeds>=0).astype(int).tolist()
            future = self.all_motors_driver_client_.call_async(req)

        # publish current states
        self.pub_states()
    
    def pub_states(self):
        """publish current motor states
        """
        # publish message
        msg = Float32MultiArray()
        msg.data = self.current_speeds.tolist()
        self.state_pub_.publish(msg)
        # info
        self.get_logger().info(f"current motor states: {self.current_speeds}")

    def set_forward_speed(self,speed: int):
        """go forward

        Args:
            speed (int): speed, 0-255
        """
        self.target_speeds = np.array([speed,]*4)

    def set_backward_speed(self,speed: int):
        """go backward

        Args:
            speed (int): speed, 0-255
        """
        self.target_speeds = np.array([-speed,]*4)

    def stop(self):
        """stop all motion
        """
        self.target_speeds = np.array([0,]*4)

    def set_directional_speed(self,angle: int,speed: int):
        # TODO
        """go in the direction of the angle passed

        Args:
            angle (int): angle in deg, 0-360
            speed (int): speed, 0-255
        """
        pass

    def rotate(self,dir: int,speed: int):
        # TODO
        """rotate the car in the specified direction at specified speed

        Args:
            dir (int): direction, [0,1]
            speed (int): speed at which to rotate, 0-255
        """
        pass

def main(args=None):
    rclpy.init(args=args)
    node = MotionControlNode()

    try:
        rclpy.spin(node)
    except Exception as e:
        print(e)
    finally:
        node.stop()
        while (node.current_speeds != np.array([0,0,0,0])).any():
            time.sleep(0.1)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()