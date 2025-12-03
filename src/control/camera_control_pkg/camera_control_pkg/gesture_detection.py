#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np
import rclpy
from control_interfaces.msg import HandGesture, HandGestureArray
from cv_bridge import CvBridge
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python.vision import (GestureRecognizer,
                                           GestureRecognizerOptions,
                                           RunningMode)
from rclpy.node import Node
from sensor_msgs.msg import Image


class MediaPipeGestureDetectorNode(Node):
    def __init__(self):
        super().__init__("mediapipe_pose_detector")

        # Subscribes to undistorted image
        self.sub_img = self.create_subscription(
            Image,
            "/undistorted_image",
            self.image_callback,
            10,
        )

        # Publisher for bounding boxes
        self.pub_bboxes = self.create_publisher(
            HandGestureArray, "/mediapipe/gesture_prediction", 10
        )

        self.bridge = CvBridge()

        # MediaPipe face detection
        base_options = python.BaseOptions(
            model_asset_path="./tutorial4/mediapipe_stuff/gesture_recognizer.task"
        )
        options = GestureRecognizerOptions(
            base_options=base_options, running_mode=RunningMode.IMAGE, num_hands=6
        )
        self.detector = GestureRecognizer.create_from_options(options)

        self.get_logger().info("MediaPipeGestureDetector node started")

    def image_callback(self, msg: Image):
        # get image from the msg
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            image_with_box = cv_image.copy()
        except Exception as e:
            self.get_logger().error(f"cv_bridge error: {e}")
            return

        # put the rectangle on there
        img_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        results = self.detector.recognize(mp_image)

        array_msg = HandGestureArray()

        # get gesture
        if results.gestures:
            for hand_idx, gestures in enumerate(results.gestures):
                # left or right hand
                handed = results.handedness[hand_idx][0].category_name

                for g in gestures:
                    hand_msg = HandGesture()
                    hand_msg.hand = handed
                    hand_msg.gesture = g.category_name
                    hand_msg.confidence = g.score
                    array_msg.gestures.append(hand_msg)

        # draw landmarks
        if results.hand_landmarks:
            for h_idx, lm_list in enumerate(results.hand_landmarks):
                lm_proto = landmark_pb2.NormalizedLandmarkList()
                lm_proto.landmark.extend(
                    [
                        landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
                        for lm in lm_list
                    ]
                )
                mp.solutions.drawing_utils.draw_landmarks(
                    image_with_box, lm_proto, mp.solutions.hands.HAND_CONNECTIONS
                )

        self.pub_bboxes.publish(array_msg)

        cv2.imshow("mediapipe_gesture_detector", image_with_box)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = MediaPipeGestureDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()