#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from driver_interfaces.msg import SetMotorSpeeds
import numpy as np
import time

class TwistMotionControlNode(Node):
    """Node that turns cmd_vel twist message to motor speed message"""

    def __init__(self):
        super().__init__("twist_motion_control")

        # params
        self.declare_parameter('wheel_radius', 0.03) # 3cm
        self.declare_parameter('half_wheelbase', 0.0585)
        self.declare_parameter('half_track', 0.08)                                                                                                                                                                                        
        self.declare_parameter('max_wheel_speed', 255) # rad/s, not calibrated yet (TODO)
        self.declare_parameter('rate', 50) # refresh rate
        self.declare_parameter('cmd_vel_timeout', 0.5)
        self.declare_parameter('wheel_order', ['fl','rl','fr','rr'])
        self.r = self.get_parameter('wheel_radius').value
        self.L = self.get_parameter('half_wheelbase').value
        self.W = self.get_parameter('half_track').value
        self.max_w = self.get_parameter('max_wheel_speed').value
        self.rate_hz = self.get_parameter('rate').value
        self.timeout_s = self.get_parameter('cmd_vel_timeout').value
        self.wheel_order = self.get_parameter('wheel_order').value

        # reliable qos profile
        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        # subscribers clients timers and such
        self.set_wheel_speeds_pub = self.create_publisher(SetMotorSpeeds, "set_motor_speeds", qos)
        self.sub_cmd = self.create_subscription(Twist, 'cmd_vel', self.cb_twist, qos)
        self.last_twist = Twist()
        self.last_ts = self.get_clock().now()
        timer_period = 1.0 / float(self.rate_hz)
        self.timer = self.create_timer(timer_period, self.timer_cb)

        # log
        self.get_logger().info('TwistMotionControlNode initialized')

    def cb_twist(self, msg: Twist):
        """on twist received, save it and the time it was received"""

        self.last_twist = msg
        self.last_ts = self.get_clock().now()

    def twist_to_wheels(self, vx, vy, wz):
        """transforms twist command to wheel speed commands"""

        R = self.r
        a = (self.L + self.W)
        w_fl = (1.0 / R) * (vx - vy - a * wz)
        w_rl = (1.0 / R) * (vx + vy - a * wz)
        w_fr = (1.0 / R) * (vx + vy + a * wz)
        w_rr = (1.0 / R) * (vx - vy + a * wz)

        return np.array([w_fl, w_rl, w_fr, w_rr])
    
    def normalize_and_clip(self, wheels):
        """normalize and clip wheel speeds to max speed"""
        
        m = np.abs(wheels).max()
        if m == 0.0:
            return np.array([0, 0, 0, 0])
        
        # if any of the speeds exceeds max speed scale it
        if m > self.max_w:
            scale = self.max_w / m
            wheels = wheels * scale

        wheels = np.clip(wheels,-self.max_w, self.max_w)

        return wheels
    
    def timer_cb(self):
        """timer callback"""

        now = self.get_clock().now()
        elapsed = (now - self.last_ts).nanoseconds * 1e-9

        if elapsed > self.timeout_s: # if last twist was too long ago set speed to zero
            wheels = np.array([0, 0, 0, 0])
        
        else:
            vx = self.last_twist.linear.x
            vy = self.last_twist.linear.y
            wz = self.last_twist.angular.z
            wheels = self.twist_to_wheels(vx, vy, wz)
            wheels = self.normalize_and_clip(wheels)

        self.set_wheel_speeds(wheels)

    def set_wheel_speeds(self,wheel_speeds):
        """send speed command to the driver

        Args:
            wheel_speeds (np.array): np array with speeds in m/s
        """
        msg = SetMotorSpeeds()
        speeds = np.floor(np.clip(wheel_speeds / self.max_w * 255.0, -255, 255)).astype(np.int16)
        msg.speeds = speeds.tolist()
        self.set_wheel_speeds_pub.publish(msg)

    def shutdown(self):
        """set speeds to zero"""
        self.set_wheel_speeds(np.array([0, 0, 0, 0]))
        time.sleep(1)


def main(args=None):
    # init
    rclpy.init(args=args)

    # initialize twist motion node
    twist_motion_control_node = TwistMotionControlNode()

    try:
        rclpy.spin(twist_motion_control_node)
    except KeyboardInterrupt:
        pass
    finally:
        twist_motion_control_node.shutdown()
        twist_motion_control_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
