import cv2
import pytest


@pytest.mark.hardware
def test_camera_capture(camera):
    ret, frame = camera.read()

    # Check if frame was captured successfully
    assert ret, "Failed to capture image."
    assert frame is not None and len(frame) > 0, "Captured image is empty."
    print("Camera successfully captured an image.")
