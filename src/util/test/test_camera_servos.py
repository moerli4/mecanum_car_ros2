import time

import pytest

DEFAULT_DELAY = 1.0


@pytest.mark.hardware
def test_servos(rb):
    time.sleep(DEFAULT_DELAY)
    rb.Ctrl_Camera_Servo(1, 30)
    time.sleep(1)
    rb.Ctrl_Camera_Servo(2, 30)
    time.sleep(DEFAULT_DELAY)
