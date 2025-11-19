import time

import pytest

DEFAULT_DELAY = 1.0
ITERATIONS = 30


@pytest.mark.hardware
def test_ultrasound_sensor(rb):
    time.sleep(DEFAULT_DELAY)
    rb.Ctrl_Ultrasound_Sensor(1)
    try:
        for _ in range(ITERATIONS):
            time.sleep(0.5)
            val = rb.Read_Ultrasound_Sensor()
            print("Ultrasound distance value:", val)
    finally:
        rb.Ctrl_Ultrasound_Sensor(0)
    time.sleep(DEFAULT_DELAY)
