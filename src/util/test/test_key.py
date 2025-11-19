import time
import pytest

DEFAULT_DELAY = 1.0
ITERATIONS = 30

@pytest.mark.hardware
def test_key(rb):
    time.sleep(DEFAULT_DELAY)
    for _ in range(ITERATIONS):
        val = rb.Read_Key_Value()
        print("Key:", val)
        time.sleep(0.5)
    time.sleep(DEFAULT_DELAY)
