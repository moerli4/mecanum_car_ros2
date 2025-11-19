import cv2
import pytest
import rclpy

from util.Raspbot_Library import Raspbot


@pytest.fixture(scope="session")
def rb():
    """Initialize rclpy and Raspbot once per test session; ensure cleanup on teardown."""
    rclpy.init()
    robot = Raspbot()
    yield robot
    # safe cleanup
    try:
        for i in range(4):
            robot.Ctrl_Car(i, 0, 0)
    except Exception:
        pass
    try:
        robot.Ctrl_Headlights_ALL(0, 0, 0)
    except Exception:
        pass
    try:
        robot.Ctrl_IR_Remote_Sensor(0)
    except Exception:
        pass
    try:
        robot.Ctrl_Ultrasound_Sensor(0)
    except Exception:
        pass
    try:
        robot.Ctrl_BEEP_Switch(0)
    except Exception:
        pass
    rclpy.shutdown()


@pytest.fixture(scope="module")
def camera():
    # Initialize video capture
    cap = cv2.VideoCapture("/dev/video0")

    if not cap.isOpened():
        raise Exception("Could not open video device.")

    yield cap

    # Release the camera when done
    cap.release()
