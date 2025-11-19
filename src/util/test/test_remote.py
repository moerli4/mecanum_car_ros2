import time
import pytest

DEFAULT_DELAY = 1.0
ITERATIONS = 30

@pytest.mark.hardware
def test_ir_remote(rb):
    time.sleep(DEFAULT_DELAY)
    rb.Ctrl_IR_Remote_Sensor(1)
    try:
        for _ in range(ITERATIONS):
            val = rb.Read_IR_Remote_Sensor()
            print("IR remote value:", val)
            time.sleep(0.5)
    finally:
        rb.Ctrl_IR_Remote_Sensor(0)
    time.sleep(DEFAULT_DELAY)
