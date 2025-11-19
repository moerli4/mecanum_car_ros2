import time
import pytest

DEFAULT_DELAY = 1.0
MOTOR_IDS = range(4)

@pytest.mark.hardware
def test_motors(rb):
    time.sleep(DEFAULT_DELAY)
    for i in MOTOR_IDS:
        rb.Ctrl_Car(i, 0, 25)
    time.sleep(1)
    for i in MOTOR_IDS:
        rb.Ctrl_Car(i, 0, 0)
    time.sleep(DEFAULT_DELAY)
