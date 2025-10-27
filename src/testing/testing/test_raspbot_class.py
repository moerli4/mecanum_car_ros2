#!/usr/bin/env python3
import rclpy
from util.Raspbot_Library import Raspbot
import time

def wait_before_and_after(func):
    """Decorator that sleeps 1 second before calling func and 1 second after."""
    def wrapper(*args, **kwargs):
        time.sleep(1)
        result = func(*args, **kwargs)
        time.sleep(1)
        return result
    return wrapper

@wait_before_and_after
def test_motors(rb: Raspbot):
    # turn all motors on
    for id in range(0,4):
        rb.Ctrl_Car(id,0,25)
    time.sleep(1)
    # turn all motors off
    for id in range(0,4):
        rb.Ctrl_Car(id,0,0)

@wait_before_and_after
def test_servos(rb: Raspbot):
    # turn both servos to 30 deg
    rb.Ctrl_Camera_Servo(1,30)
    time.sleep(1)
    rb.Ctrl_Camera_Servo(2,30)

@wait_before_and_after
def test_headlights(rb: Raspbot):
    # test Headlights_ALL function
    rb.Ctrl_Headlights_ALL(126,0,0)
    time.sleep(1)
    rb.Ctrl_Headlights_ALL(0,126,0)
    time.sleep(1)
    rb.Ctrl_Headlights_ALL(0,0,126)
    time.sleep(1)
    rb.Ctrl_Headlights_ALL(0,0,0)

    # test Headlights_ID function
    for id_ in range(1,15):
        rb.Ctrl_Headlights_ID(id_,126,126,126)
        time.sleep(0.2)
    time.sleep(1)
    for id_ in list(range(14,0,-1)):
        rb.Ctrl_Headlights_ID(id_,0,0,0)
        time.sleep(0.2)
    
@wait_before_and_after
def test_beep_switch(rb: Raspbot):
    rb.Ctrl_BEEP_Switch(1)
    time.sleep(0.5)
    rb.Ctrl_BEEP_Switch(0)

@wait_before_and_after
def test_ir_track_sensor(rb:Raspbot):
    for i in range(30):
        print(rb.Read_IR_Sensor())
        time.sleep(0.5)

@wait_before_and_after
def test_ir_remote(rb:Raspbot):
    rb.Ctrl_IR_Remote_Sensor(1)
    for i in range(30):
        print(rb.Read_IR_Remote_Sensor())
        time.sleep(0.5)
    rb.Ctrl_IR_Remote_Sensor(0)

@wait_before_and_after
def test_ultrasound_sensor(rb:Raspbot):
    rb.Ctrl_Ultrasound_Sensor(1)
    for i in range(30):
        time.sleep(0.5)
        print(rb.Read_Ultrasound_Sensor())
    rb.Ctrl_Ultrasound_Sensor(0)

@wait_before_and_after
def test_key(rb:Raspbot):
    for i in range(30):
        print(rb.Read_Key_Value())
        time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    
    ## test raspbot init
    rb = Raspbot()
    print("Raspbot Object Created\n")

    ## test Ctrl_Car
    input("Press Enter To Test Motors")
    test_motors(rb)
    print("Testing Motors Done\n")

    # test Ctrl_Camera_Servo
    input("Press Enter To Test Servos")
    test_servos(rb)
    print("Testing Servos Done\n")

    # test Ctrl_Headlights_ALL and Ctrl_Headlights_ID
    input("Press Enter to Test Headlights")
    test_headlights(rb)
    print("Testing Headlights Done\n")

    # test Ctrl_BEEP_Switch
    input("Press Enter to Test Beep Switch")
    test_beep_switch(rb)
    print("Testing Beep Switch Done\n")


    # test IR track Sensor
    input("Press Enter to Test IR Track Sensor")
    test_ir_track_sensor(rb)
    print("Testing IR Track Sensor\n")

    # test IR remote sensor
    input("Press Enter to IR Remote Sensor")
    test_ir_remote(rb)
    print("Testing IR Remote Sensor Done\n")

    # test Ultrasound Sensor
    input("Press Enter to Test Ultrasound Sensor")
    test_ultrasound_sensor(rb)
    print("Testing Ultrasound Sensor Done\n")

    # test Key 
    input("Press Enter to Test Key")
    test_key(rb)
    print("Testing Key Done\n")

    rclpy.shutdown()

if __name__ == "__main__":
    main()