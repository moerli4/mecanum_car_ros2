#!/usr/bin/env python3
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage


class CameraDataDriverNode(Node):
    """Publisher Node to publish the camera data as a compressed jpeg"""

    def __init__(self):
        super().__init__("camera_data_driver")

        # Publisher for compressed images
        self.publisher_ = self.create_publisher(
            CompressedImage, "camera/compressed_image", 10
        )

        # Initialize video capture
        self.cap = cv2.VideoCapture("/dev/video0")

        if not self.cap.isOpened():
            self.get_logger().error("Error: Could not open video device.")
            rclpy.shutdown()
            return

        # Timer to periodically capture and publish images
        self.timer = self.create_timer(0.1, self.capture_and_publish)

        self.get_logger().info("CameraDataDriverNode initiated")

    def capture_and_publish(self):
        ret, frame = self.cap.read()
        if ret:
            # Encode the image to JPEG format
            _, buffer = cv2.imencode(".jpg", frame)
            compressed_image = CompressedImage()
            compressed_image.header.stamp = self.get_clock().now().to_msg()
            compressed_image.format = "jpeg"
            compressed_image.data = buffer.tobytes()

            # Publish the compressed image
            self.publisher_.publish(compressed_image)
            self.get_logger().info("Published compressed image.")
        else:
            self.get_logger().error("Failed to capture image.")

    def destroy_node(self):
        self.cap.release()  # Release the video capture when shutting down
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraDataDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
