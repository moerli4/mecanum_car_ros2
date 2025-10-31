#!/usr/bin/env python3
import time
import rclpy
from util.Raspbot_Library import Raspbot

# Constants
MOTOR_IDS = range(4)          # motor channel IDs 0-3
HEADLIGHT_IDS = range(1, 15)  # headlight IDs 1-14
ITERATIONS = 30               # number of sensor reads
DEFAULT_DELAY = 1.0           # default decorator delay in seconds

def wait_before_and_after(delay=DEFAULT_DELAY):
    """
    Decorator that sleeps for `delay` seconds before calling the wrapped function and `delay` seconds after
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            try:
                return func(*args, **kwargs)
            finally:
                time.sleep(delay)
        return wrapper
    return decorator

@wait_before_and_after()
def test_motors(rb):
    """
    Test motors
    """
    # Start all motors at speed 25
    for i in MOTOR_IDS:
        rb.Ctrl_Car(i, 0, 25)
    time.sleep(1)
    # Stop all motors
    for i in MOTOR_IDS:
        rb.Ctrl_Car(i, 0, 0)

@wait_before_and_after()
def test_servos(rb):
    """
    Test camera servos by setting them to 30 deg
    """
    rb.Ctrl_Camera_Servo(1, 30)
    time.sleep(1)
    rb.Ctrl_Camera_Servo(2, 30)

@wait_before_and_after()
def test_headlights(rb):
    """
    Test both Headlight functions.
    """
    try:
        # Demonstrate ALL-color control (red, green, blue)
        rb.Ctrl_Headlights_ALL(126, 0, 0)
        time.sleep(1)
        rb.Ctrl_Headlights_ALL(0, 126, 0)
        time.sleep(1)
        rb.Ctrl_Headlights_ALL(0, 0, 126)
        time.sleep(1)
    finally:
        rb.Ctrl_Headlights_ALL(0, 0, 0)  # turn all off

    try:
        # Light each ID in sequence
        for id_ in HEADLIGHT_IDS:
            rb.Ctrl_Headlights_ID(id_, 126, 126, 126)
            time.sleep(0.5)
        # Turn them off in reverse order
        for id_ in reversed(list(HEADLIGHT_IDS)):
            rb.Ctrl_Headlights_ID(id_, 0, 0, 0)
            time.sleep(0.5)
    finally:
        rb.Ctrl_Headlights_ALL(0, 0, 0)  # turn all off

@wait_before_and_after()
def test_beep_switch(rb):
    """
    Toggle beep to verify buzzer works
    """
    rb.Ctrl_BEEP_Switch(1)
    time.sleep(0.5)
    rb.Ctrl_BEEP_Switch(0)

@wait_before_and_after()
def test_ir_track_sensor(rb):
    """
    Read IR tracking sensor repeatedly and print values
    """
    for _ in range(ITERATIONS):
        # Print to console; hardware method returns sensor values
        print("IR track value:", rb.Read_IR_Sensor())
        time.sleep(0.5)

@wait_before_and_after()
def test_ir_remote(rb):
    """
    Enable IR remote sensor, read repeatedly, then disable it
    """
    rb.Ctrl_IR_Remote_Sensor(1)
    try:
        for _ in range(ITERATIONS):
            print("IR remote value:", rb.Read_IR_Remote_Sensor())
            time.sleep(0.5)
    finally:
        rb.Ctrl_IR_Remote_Sensor(0)

@wait_before_and_after()
def test_ultrasound_sensor(rb):
    """
    Enable ultrasound sensor, read distances repeatedly, then disable it
    """
    rb.Ctrl_Ultrasound_Sensor(1)
    try:
        for _ in range(ITERATIONS):
            time.sleep(0.5)
            print("Ultrasound distance value:", rb.Read_Ultrasound_Sensor())
    finally:
        rb.Ctrl_Ultrasound_Sensor(0)

@wait_before_and_after()
def test_key(rb):
    """
    Read key/button value to verify input switches
    """
    for _ in range(ITERATIONS):
        print("Key:", rb.Read_Key_Value())
        time.sleep(0.5)

def safe_cleanup(rb):
    """
    Attempt to return hardware to a safe state:
    - stop motors
    - turn off headlights
    - disable sensors and buzzer
    """
    try:
        for i in MOTOR_IDS:
            rb.Ctrl_Car(i, 0, 0)
    except Exception:
        pass

    try:
        rb.Ctrl_Headlights_ALL(0, 0, 0)
    except Exception:
        pass

    try:
        rb.Ctrl_IR_Remote_Sensor(0)
    except Exception:
        pass

    try:
        rb.Ctrl_Ultrasound_Sensor(0)
    except Exception:
        pass

    try:
        rb.Ctrl_BEEP_Switch(0)
    except Exception:
        pass

def main(args=None):
    """
    Main test sequence:
    - initialize rclpy and Raspbot
    - prompt user before each test
    - run tests with safe cleanup on exceptions or user interrupt
    """
    rclpy.init(args=args)
    rb = Raspbot()
    print("Raspbot Object Created\n")

    try:
        input("Press Enter To Test Motors")
        test_motors(rb)

        input("Press Enter To Test Servos")
        test_servos(rb)

        input("Press Enter to Test Headlights")
        test_headlights(rb)

        input("Press Enter to Test Beep Switch")
        test_beep_switch(rb)

        input("Press Enter to Test IR Track Sensor")
        test_ir_track_sensor(rb)

        input("Press Enter To IR Remote Sensor")
        test_ir_remote(rb)

        input("Press Enter to Test Ultrasound Sensor")
        test_ultrasound_sensor(rb)

        input("Press Enter to Test Key")
        test_key(rb)

    except KeyboardInterrupt:
        print("Interrupted by user — performing safe cleanup.")
    except Exception:
        print("Error during tests, performing safe cleanup.")
    finally:
        # Ensure hardware is left in a safe state and shutdown rclpy
        safe_cleanup(rb)
        rclpy.shutdown()

if __name__ == "__main__":
    main()
    