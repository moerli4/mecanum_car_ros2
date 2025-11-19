import time

import pytest

DEFAULT_DELAY = 1.0


@pytest.mark.hardware
def test_beep_switch(rb):
    time.sleep(DEFAULT_DELAY)
    rb.Ctrl_BEEP_Switch(1)
    time.sleep(0.5)
    rb.Ctrl_BEEP_Switch(0)
    time.sleep(DEFAULT_DELAY)
