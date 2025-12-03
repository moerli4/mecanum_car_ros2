#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np
import rclpy
from control_interfaces.msg import FaceBoundingBoxArray, HandGestureArray, PoseLandmarks
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
from PIL import Image, ImageTk
import tkinter as tk
import threading


class ImageHandlerNode(Node):
    """Node to display all the images with the detected bounding boxes etc.
    Only run if a display is connected to the Raspberry Pi.
    """

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
        self.frame = None

        # Subscriber for face detection
        self.face_det_sub_ = self.create_subscription(
            FaceBoundingBoxArray,
            "/mediapipe/face_detection_bboxes",
            self.face_bbox_callback,
            qos_profile,
        )

        # Subscriber for pose detection
        self.pose_det_sub_ = self.create_subscription(
            PoseLandmarks,
            "/mediapipe/pose_detection_info",
            self.pose_landmarks_callback,
            qos_profile,
        )

        # Subscriber for gesture detection
        self.gesture_det_sub_ = self.create_subscription(
            HandGestureArray,
            "/mediapipe/gesture_detection_info",
            self.gesture_info_callback,
            qos_profile,
        )

        # overlay info dict
        self.overlays = {
            "face_bboxes": None,
            "pose_landmarks": None,
            "gesture_infos": None,
        }

        # ros2 bridge
        self.bridge = CvBridge()

        ## create a small gui ----------------
        # Initialize GUI components
        self.root = tk.Tk()
        self.root.title("Overlay Selector")
        self.root.geometry("800x600")  # Set the window size to 800x600
        self.root.title("Camera Stuff Visualization")

        # Checkbox states for overlays
        self.overlay_checks = [tk.BooleanVar(value=False) for _ in self.overlays]

        # Frame for checkboxes
        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.pack(side=tk.BOTTOM)

        # Create checkboxes for overlays
        for i, text in enumerate(self.overlays.keys()):
            checkbox = tk.Checkbutton(
                self.checkbox_frame,
                text=text,
                variable=self.overlay_checks[i],
                command=self.update_gui,
            )
            checkbox.pack(anchor="w")

        # Label for displaying the image
        self.label = tk.Label(self.root)
        self.label.pack()

        ## spin ros as a daemon --------------
        self.ros_thread = threading.Thread(target=self.run_ros_spin)

        ## log -------------------------------
        self.get_logger().info("Image handler node started")

    def image_callback(self, msg: CompressedImage):
        # msg.data is bytes of the JPEG image
        np_arr = np.frombuffer(msg.data, dtype=np.uint8)
        self.frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # BGR OpenCV image

        if self.frame is None:
            self.get_logger().error("Failed to decode image")
            return

    def face_bbox_callback(self, msg: FaceBoundingBoxArray):
        self.overlays["face_bboxes"] = msg.faces

    def pose_landmarks_callback(self, msg: PoseLandmarks):
        self.overlays["pose_landmarks"] = [msg.x, msg.y, msg.z]

    def gesture_info_callback(self, msg: HandGestureArray):
        self.overlays["gesture_infos"] = msg.gestures

    def update_gui(self):
        # process images
        if self.frame is not None:
            display_image = self.frame.copy()

            # Apply selected overlays
            for is_checked, overlay_name in zip(
                self.overlay_checks, self.overlays.keys()
            ):
                if is_checked and self.overlays[overlay_name] is not None:
                    match overlay_name:
                        case "face_bboxes":
                            pass
                        case "pose_landmarks":
                            pass
                        case "gesture_infos":
                            pass

            # Convert to suitable format for Tkinter
            display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(display_image))
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        else:
            self.label.configure(image="")  # Clear the image if none is available

        # Schedule the next gui update
        self.root.after(100, self.update_gui)

    def run_gui(self):
        self.update_gui()  # Start the GUI update loop
        self.root.mainloop()

    def run_ros_spin(self):
        while rclpy.ok():
            rclpy.spin_once(self)


def main(args=None):
    rclpy.init(args=args)
    node = ImageHandlerNode()
    try:
        node.ros_thread.start()
        node.run_gui()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
