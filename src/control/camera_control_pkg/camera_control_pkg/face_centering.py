#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from control_interfaces.msg import FaceBoundingBoxArray
from driver_interfaces.srv import SetServo
import numpy as np
import time
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy


class FaceCenteringController(Node):
    """Node to center detected faces using camera servos"""
    
    def __init__(self):
        super().__init__("face_centering_controller")

        # Use reliable qos profile
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Subscribe to face detection results
        self.face_subscriber = self.create_subscription(
            FaceBoundingBoxArray,
            "/mediapipe/face_detection_bboxes",
            self.face_callback,
            qos_profile,
        )

        # controller params
        self.position_error_x = 0
        self.position_error_y = 0
        self.threshold = 0.1
        self.angle_x = 90
        self.angle_y = 50

        # Create a service client for setting the servo
        self.servo_client = self.create_client(SetServo, "set_camera_servo")
        self.logger = self.get_logger()
        
        # go to default_position
        self.send_request(1,90)
        self.send_request(2,50)
        time.sleep(1)

        # Ensure the server is available before making requests
        while not self.servo_client.wait_for_service(timeout_sec=1.0):
            self.logger.info("Waiting for Servo service to be available...")
        
    def face_callback(self, msg: FaceBoundingBoxArray):
        # if any faces are detected
        if msg.faces:
            # assume we want to center on the first detected face
            face = msg.faces[0]

            # Calculate the center of the face box for x
            face_center_x = (face.x1 + face.x2) / 2
            self.position_error_x = (face_center_x - 1 / 2)

            # Calculate the center of the face box for y
            face_center_y = (face.y1 + face.y2) / 2
            self.position_error_y = (face_center_y - 1 / 2)

    def center(self):
        if abs(self.position_error_x) > self.threshold:
            self.angle_x += -1 if self.position_error_x>0 else 1 # how many degrees per update
            self.send_request(1,self.angle_x)
        if abs(self.position_error_y) > self.threshold:
            self.angle_y += -1 if self.position_error_y>0 else 1
            self.send_request(2,self.angle_y)
        
    def send_request(self,id,angle):
        # send x request
        request = SetServo.Request()
        request.id = 1
        if id == 1:
            angle = np.clip(angle, 0, 100) 
        elif id == 2:
            angle = np.clip(angle, 0, 180) 
        request.set_angle = int(angle)    

        # call service
        self.logger.info(f"Sending servo command: id={request.id}, angle={request.set_angle}")
        future = self.servo_client.call_async(request)
        rclpy.spin_until_future_complete(self,future)


def main(args=None):
    rclpy.init(args=args)
    node = FaceCenteringController()
    try:
        while rclpy.ok():
            node.center()
            rclpy.spin_once(node,timeout_sec=1)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
