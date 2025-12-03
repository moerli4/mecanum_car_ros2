#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np
import rclpy
from cv_bridge import CvBridge 
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy

class ImageHandlerNode(Node):
    def __init__(self):
        super().__init__("image_handler_node")

        # Use reliable qos profile for camera image
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Subscribes to the compressed image from the driver
        self.compressed_image = self.create_subscription(
            CompressedImage,
            "camera/compressed_image",
            self.image_callback,
            qos_profile,
        )

        # ros2 bridge
        self.bridge = CvBridge()

        self.get_logger().info("Image handler node started")

    def image_callback(self, msg: CompressedImage):
        # msg.data is bytes of the JPEG image
        np_arr = np.frombuffer(msg.data, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # BGR OpenCV image

        if frame is None:
            self.get_logger().error('Failed to decode image')
            return

        self.get_logger().info(f'Image received')

        # show image
        cv2.imshow('received image', frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ImageHandlerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()