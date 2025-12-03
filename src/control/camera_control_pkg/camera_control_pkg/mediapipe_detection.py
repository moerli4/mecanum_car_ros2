#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np
import rclpy
from control_interfaces.msg import (
    FaceBoundingBox,
    FaceBoundingBoxArray,
    HandGesture,
    HandGestureArray,
    PoseLandmarks,
)
from cv_bridge import CvBridge
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import (
    GestureRecognizer,
    GestureRecognizerOptions,
    RunningMode,
)
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage


class MediapipeDetectionNode(Node):
    """Node to detect faces, gestures and poses and publish their coordinates and info"""

    def __init__(self):
        super().__init__("mediapie_detection_node")

        # Use reliable qos profile
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # ros2 bridge
        self.bridge = CvBridge()

        ## IMAGE HANDLING --------------------
        # Subscribes to the compressed image from the driver
        self.compressed_image_ = self.create_subscription(
            CompressedImage,
            "camera/compressed_image",
            self.image_callback,
            qos_profile,
        )

        ## FACE DETECTION --------------------
        # Publisher for face detection
        self.face_det_publisher_ = self.create_publisher(
            FaceBoundingBoxArray, "/mediapipe/face_detection_bboxes", qos_profile
        )
        # MediaPipe face detection
        base_options = python.BaseOptions(
            model_asset_path="./src/control/camera_control_pkg/mediapipe_lib/blaze_face_short_range.tflite"
        )
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.face_detector = vision.FaceDetector.create_from_options(options)

        ## POSE DETECTION --------------------
        # Publisher for pose detection
        self.pose_det_publisher_ = self.create_publisher(
            PoseLandmarks, "/mediapipe/pose_detection_info", qos_profile
        )
        base_options = python.BaseOptions(
            model_asset_path="./src/control/camera_control_pkg/mediapipe_lib/pose_landmarker_full.task"
        )
        options = vision.PoseLandmarkerOptions(
            base_options=base_options, output_segmentation_masks=False
        )
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)

        ## GESTURE DETECTION -----------------
        # Publisher for gesture detection
        self.gesture_det_publisher_ = self.create_publisher(
            HandGestureArray, "/mediapipe/gesture_detection_info", qos_profile
        )
        # MediaPipe gesture detection
        base_options = python.BaseOptions(
            model_asset_path="./src/control/camera_control_pkg/mediapipe_lib/gesture_recognizer.task"
        )
        options = GestureRecognizerOptions(
            base_options=base_options, running_mode=RunningMode.IMAGE, num_hands=6
        )
        self.gesture_detector = GestureRecognizer.create_from_options(options)

        # log
        self.get_logger().info("Mediapipe detector node started")

    def image_callback(self, msg: CompressedImage):
        # msg.data is bytes of the JPEG image
        np_arr = np.frombuffer(msg.data, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # decode
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # transform to rgb

        # log
        if frame is None:
            self.get_logger().error("Failed to decode image")
            return

        # do face detection
        self.face_detection(frame)

        # do pose detection
        self.pose_detection(frame)

        # do gesture detection
        self.gesture_detection(frame)

    def face_detection(self, cv_image):
        # do face detection with mediapipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_image)
        results = self.face_detector.detect(mp_image)
        w,h,_ = cv_image.shape

        # create bbox array msg
        bbox_array_msg = FaceBoundingBoxArray()

        # iterate over all detected faces
        if results.detections:
            for det in results.detections:
                # create bbox msg
                bbox = det.bounding_box

                x1 = int(bbox.origin_x)
                y1 = int(bbox.origin_y)
                x2 = int(bbox.origin_x + bbox.width)
                y2 = int(bbox.origin_y + bbox.height)

                fbb = FaceBoundingBox()
                fbb.x1 = x1/w
                fbb.x2 = x2/w
                fbb.y1 = y1/h
                fbb.y2 = y2/h

                # append bbox msg to bbox array msg
                bbox_array_msg.faces.append(fbb)

        # publish
        self.face_det_publisher_.publish(bbox_array_msg)

    def pose_detection(self, cv_image):
        # do pose detection with mediapipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_image)
        results = self.pose_detector.detect(mp_image)
        
        # create landmarks message
        pose_msg = PoseLandmarks()

        # iterate over detected landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks[0]

            # append markers to the msg
            for lm in landmarks:
                pose_msg.x.append(lm.x)
                pose_msg.y.append(lm.y)
                pose_msg.z.append(lm.z)

        # publish
        self.pose_det_publisher_.publish(pose_msg)

    def gesture_detection(self, cv_image):
        # do gesture detection with mediapipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_image)
        results = self.gesture_detector.recognize(mp_image)

        # create gesture message
        array_msg = HandGestureArray()

        # iterate over detected gestures
        if results.gestures and results.hand_landmarks:
            for hand_idx, (gestures,landmarks) in enumerate(zip(results.gestures,results.hand_landmarks)):
                # left or right hand
                handed = results.handedness[hand_idx][0].category_name

                # append info to message
                for g in gestures:
                    hand_msg = HandGesture()
                    hand_msg.hand = handed
                    hand_msg.x = [lm.x for lm in landmarks]
                    hand_msg.y = [lm.y for lm in landmarks]
                    hand_msg.z = [lm.z for lm in landmarks]
                    hand_msg.gesture = g.category_name
                    hand_msg.confidence = g.score
                    array_msg.gestures.append(hand_msg)

        # publish
        self.gesture_det_publisher_.publish(array_msg)


def main(args=None):
    rclpy.init(args=args)
    node = MediapipeDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
