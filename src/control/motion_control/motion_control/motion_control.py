#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time

from interfaces.srv import SetMotor
from std_msgs.msg import Float32MultiArray

MAX_SPEED = 255
SLEW_STEP = 10         # TODO: max change per call to avoid hardware damage

class MotionControlNode(Node):
    """Node for Motion Control"""

    def __init__(self):
        super().__init__("motion_control_node")

        # create client to drivers
        self.motor_driver_client_ = self.create_client(SetMotor, "set_motor")

        # create publisher for current states
        self.state_pub_ = self.create_publisher(Float32MultiArray, 'motor_states', 10)
        self.timer = self.create_timer(0.5, self.pub_states)

        # class parameters
        self.current_speeds = [0, 0, 0, 0]


    def pub_states(self):
        """publish current motor states
        """
        # publish message
        msg = Float32MultiArray()
        msg.data = self.current_speeds
        self.state_pub_.publish(msg)
        # info
        self.get_logger().info(f"current motor states: {self.current_speeds}")

    def set_motor(self, index: int, speed: int):
        """helper function to set motor speed and update class parameters

        Args:
            index (int): index of the motor to set
            speed (int): turn speed, -255 - 255
        """
        # sanitize inputs
        speed = max(-MAX_SPEED, min(MAX_SPEED, int(speed)))

        self.get_logger().info(f"trying to set speed to: {speed}")

        # call drivers
        req = SetMotor.Request()
        req.id = index
        req.speed = abs(speed)
        req.dir = int(speed>=0)
        future = self.motor_driver_client_.call_async(req)

        # update parameters
        self.current_speeds[index] = speed
        
        return future
    
    def set_forward_speed(self,speed: int):
        """go forward

        Args:
            speed (int): speed, 0-255
        """
        for i in range(4):
            self.set_motor(i, speed)

    def set_backward_speed(self,speed: int):
        """go backward

        Args:
            speed (int): speed, 0-255
        """
        for i in range(4):
            self.set_motor(i, -speed)

    def stop(self):
        """stop all motion
        """
        for i in range(4):
            self.set_motor(i, 0)

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
    
    node.set_forward_speed(10)
    time.sleep(2)
    
    node.set_backward_speed(10)
    time.sleep(2)

    node.stop()
    time.sleep(1)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()