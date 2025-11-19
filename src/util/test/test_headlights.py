import time
import pytest

DEFAULT_DELAY = 1.0
HEADLIGHT_IDS = range(1, 15)

@pytest.mark.hardware
def test_headlights(rb):
    time.sleep(DEFAULT_DELAY)
    try:
        rb.Ctrl_Headlights_ALL(126, 0, 0)
        time.sleep(1)
        rb.Ctrl_Headlights_ALL(0, 126, 0)
        time.sleep(1)
        rb.Ctrl_Headlights_ALL(0, 0, 126)
        time.sleep(1)
    finally:
        rb.Ctrl_Headlights_ALL(0, 0, 0)

    time.sleep(0.2)
    try:
        for id_ in HEADLIGHT_IDS:
            rb.Ctrl_Headlights_ID(id_, 126, 126, 126)
            time.sleep(0.5)
        for id_ in reversed(list(HEADLIGHT_IDS)):
            rb.Ctrl_Headlights_ID(id_, 0, 0, 0)
            time.sleep(0.5)
    finally:
        rb.Ctrl_Headlights_ALL(0, 0, 0)
    time.sleep(DEFAULT_DELAY)
