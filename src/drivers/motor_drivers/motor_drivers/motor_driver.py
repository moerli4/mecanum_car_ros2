#!/usr/bin/env python3
import time

import numpy as np
import rclpy
from driver_interfaces.msg import SetMotorSpeeds
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from rclpy.node import Node

from util.Raspbot_Library import Raspbot

def scale_to_range(arr: np.ndarray, m: float) -> np.ndarray:
    """scales a numpy array to [-m,m]

    Args:
        arr (np.array): array to be scaled
        m (float): max_value

    Returns:
        np.ndarray: scaled array
    """
    arr = np.asarray(arr, dtype=float)
    max_abs = np.max(np.abs(arr))
    if max_abs == 0 or max_abs <= m:
        return arr.copy()
    return arr * (m / max_abs)

class MotorDriverNode(Node):
    def __init__(self):
        super().__init__("motor_driver")
        self.raspbot_ = Raspbot()

        # params
        self.declare_parameter("timeout", 0.5)  # seconds before stopping if no cmd
        self.declare_parameter("max_pwm", 200)  # limit to some value [0,255] for hardware safety
        self.timeout = float(self.get_parameter("timeout").value)
        self.max_pwm = self.get_parameter("max_pwm")

        # last command timestamp and values
        self._last_cmd_time = self.get_clock().now()
        self._last_speeds = np.array([0, 0, 0, 0])

        # subscriptions
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self.sub_speeds = self.create_subscription(
            SetMotorSpeeds, "set_motor_speeds", self.cb_speeds, qos_profile
        )

        # timer for timeout checking
        self.create_timer(1 / 60, self._timer_cb)  # 60 Hz

        # log
        self.get_logger().info(f"MotorDriverNode initiated")

    def cb_speeds(self, msg: SetMotorSpeeds):
        """callback on set motor speed message received"""
        data = np.array(msg.speeds) * -1  # speeds are inverted
        data = scale_to_range(data,self.max_pwm)
        self._last_speeds = data.astype(int)
        self._last_cmd_time = self.get_clock().now()
        self._apply_to_hardware()

    def _apply_to_hardware(self):
        """apply to hardware"""
        for i, (d, s) in enumerate(
            zip(
                (self._last_speeds >= 0).astype(int).tolist(),  # directions
                np.abs(self._last_speeds).astype(int).tolist(),  # speeds
            )
        ):
            try:
                self.raspbot_.Ctrl_Car(i, int(d), int(s))
            except Exception as e:
                self.get_logger().error(f"Error applying to motor {i}: {e}")

    def _timer_cb(self):
        """timer callback"""
        # stop motors if timeout exceeded
        elapsed = (self.get_clock().now() - self._last_cmd_time).nanoseconds * 1e-9
        if elapsed > self.timeout:
            # zero speeds
            if (self._last_speeds != 0).any():
                self.get_logger().info("Command timeout: stopping motors")
                self._last_speeds = np.array([0, 0, 0, 0])
                self._apply_to_hardware()


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()
    try:
        rclpy.spin(node)
    finally:
        # ensure motors stopped on shutdown
        node._last_speeds = np.array([0, 0, 0, 0])
        node._apply_to_hardware()
        time.sleep(1)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
