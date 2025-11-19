import time

import pytest

DEFAULT_DELAY = 1.0
ITERATIONS = 30


@pytest.mark.hardware
def test_ir_track_sensor(rb):
    time.sleep(DEFAULT_DELAY)
    for _ in range(ITERATIONS):
        val = rb.Read_IR_Sensor()
        print("IR track value:", val)
        time.sleep(0.5)
    time.sleep(DEFAULT_DELAY)
