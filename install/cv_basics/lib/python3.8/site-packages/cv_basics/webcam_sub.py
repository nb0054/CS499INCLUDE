# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
  
# Import the necessary libraries
import os.path

import numpy as np
import time
import cv2.dnn
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
 
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image, 
      'depth_camera/image_raw', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)

    # Code for object detection
    classes = open(os.path.abspath('/home/sadurac/dev_ws/src/YOLOcfg/coco.names'), 'rt').read().strip().split('\n')
    net = cv2.dnn_DetectionModel(os.path.abspath('/home/sadurac/dev_ws/src/YOLOcfg/frozen_inference_graph.pb'),
                                 os.path.abspath('/home/sadurac/dev_ws/src/YOLOcfg/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'))
    net.setInputSize(320, 320)
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    classIds, confs, bbox = net.detect(current_frame, confThreshold=0.5)
    print(classIds,confs,bbox)
    if len(classIds) != 0:
      for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
        cv2.rectangle(current_frame, box, color=(0,255,0), thickness=2)
        cv2.putText(current_frame, classes[classId-1].upper(),(box[0]-10, box[1]-30), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2 )
    cv2.imshow("Camera", current_frame)
    cv2.waitKey(1)

def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
