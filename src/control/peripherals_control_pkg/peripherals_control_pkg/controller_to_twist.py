#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

def apply_deadzone(value, deadzone):
    return 0.0 if abs(value) <= deadzone else value

class ControllerToTwistNode(Node):
    def __init__(self):
        super().__init__('controller_to_twist')

        self.declare_parameter('axis_linear_x', 0)
        self.declare_parameter('axis_linear_y', 1)
        self.declare_parameter('axis_angular_yaw', 3)
        self.declare_parameter('deadzone', 0.1)
        self.declare_parameter('invert_linear_x', False)
        self.declare_parameter('invert_linear_y', False)
        self.declare_parameter('invert_angular', False)

        self.declare_parameter('boost_button', 5)
        self.declare_parameter('boost_value', 1.0)

        self.declare_parameter('enable_button', 2)
        
        self.declare_parameter('scale_speed', 0.5)
        self.declare_parameter('axis_change_scale', 7)
        self.declare_parameter('change_scale_increment', 0.05)

        p = self.get_parameters([
            'axis_linear_x','axis_linear_y','axis_angular_yaw',
            'deadzone','invert_linear_x','invert_linear_y','invert_angular',
            'boost_button','boost_value',
            'enable_button',
            'scale_speed','axis_change_scale','change_scale_increment'
        ])

        # speed
        self.axis_linear_x = p[0].value
        self.axis_linear_y = p[1].value
        self.axis_angular_yaw = p[2].value
        self.deadzone = p[3].value
        self.invert_linear_x = p[4].value
        self.invert_linear_y = p[5].value
        self.invert_angular = p[6].value
        # boost button
        self.boost_button = p[7].value
        self.boost_value = p[8].value
        # enable button
        self.enable_button = p[9].value
        self.enabled = True
        self.enable_button_pressed = False
        # scale speed
        self.scale_speed = p[10].value
        self.axis_change_scale = p[11].value
        self.change_scale_increment = p[12].value
        self.change_scale_pressed = False

        self.sub = self.create_subscription(Joy, 'joy', self.joy_cb, 10)
        self.pub_twist = self.create_publisher(Twist, 'cmd_vel', 10)

        self.get_logger().info("Controller Manager Node initialized")

    def joy_index(self, arr, idx):
        """get the controller input at certain index with error handling"""
        try:
            return arr[idx]
        except Exception as e:
            self.get_logger().warn(e)
            return 0.0

    def joy_cb(self, msg: Joy):
        """on joystick message received"""
        # enable or disable the controller
        b = int(self.joy_index(msg.buttons, self.enable_button))
        if b != 0 and not self.enable_button_pressed:
            self.enable_button_pressed = True
            self.enabled = not self.enabled
            self.get_logger().info(f"enabled state set to: {self.enabled}")
        elif b == 0:
            self.enable_button_pressed = False

        # change speed scaler if pressed
        ax_change_scale = float(self.joy_index(msg.axes, self.axis_change_scale))
        if ax_change_scale != 0.0 and not self.change_scale_pressed:
            self.change_scale_pressed = True
            try:
                self.scale_speed += self.change_scale_increment * ax_change_scale
                self.get_logger().info(f"new speed set: {self.scale_speed}")
            except Exception as e:
                self.get_logger().warn(e)
        elif ax_change_scale == 0.0:
            self.change_scale_pressed = False

        # read axes
        ax_x = float(self.joy_index(msg.axes, self.axis_linear_x))
        ax_y = float(self.joy_index(msg.axes, self.axis_linear_y))
        ax_yaw = float(self.joy_index(msg.axes, self.axis_angular_yaw))

        # invert axis if needed
        if self.invert_linear_x: ax_x = -ax_x
        if self.invert_linear_y: ax_y = -ax_y
        if self.invert_angular: ax_yaw = -ax_yaw

        # apply deadzone
        ax_x = apply_deadzone(ax_x, self.deadzone)
        ax_y = apply_deadzone(ax_y, self.deadzone)
        ax_yaw = apply_deadzone(ax_yaw, self.deadzone)

        # init return message
        twist = Twist()

        # read boost button
        boost_pressed = int(self.joy_index(msg.buttons, self.boost_button)) != 0

        # compute speed scales
        _add = self.boost_value if boost_pressed else 0.0
        sx = self.scale_speed + _add
        sy = self.scale_speed + _add
        sa = self.scale_speed + _add + 3.5

        # apply scales to axes
        if self.enabled:
            twist.linear.x = ax_y * sy
            twist.linear.y = ax_x * sx
            twist.angular.z = ax_yaw * sa
        else:
            twist.linear.x = twist.linear.y = twist.angular.z = 0.0

        self.pub_twist.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ControllerToTwistNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
