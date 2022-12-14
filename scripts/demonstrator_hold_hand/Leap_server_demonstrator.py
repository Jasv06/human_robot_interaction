import socket
import sys
import numpy as np
import rospy
import time 
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32
import struct 

localIP = "127.0.0.1"
Port = 57410

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((localIP, Port))
   
def leap_data():
  
  rospy.init_node('Leap_data', anonymous = False)  
  
  """Number of hands"""
  pub_number_of_hands = rospy.Publisher('HandNumber', Float32, queue_size = 1)
  
  """Hand state"""
  pub_hand_state = rospy.Publisher('hand_state', Float32, queue_size = 1)
  
  """hand publishers"""

  pub_hand_id = rospy.Publisher('hand_id', Float32, queue_size = 1)
 
  pub_palm_position_stable = rospy.Publisher('hand_position_stable', Point, queue_size = 1)
 
  pub_life_of_hand = rospy.Publisher('life_of_hand', Float32, queue_size = 1)
  
  rate = rospy.Rate(50)
  
  while not rospy.is_shutdown():
  
     coordinates = Point() 
    
     data, address = s.recvfrom(4096)
          
     data = struct.unpack('<8f', data)      
     
     number_of_hand_in_frame = data[0]
     
     strength = data[1]
     
     hand_identifier = data[2]
          
     coordinates.x = data[3]*0.001
     coordinates.y = data[4]*0.001
     coordinates.z = data[5]*0.001
     
     life_of_hand_in_sensor = data[6]
          
     pub_number_of_hands.publish(number_of_hand_in_frame)
     pub_hand_state.publish(strength)
     pub_hand_id.publish(hand_identifier)
     pub_palm_position_stable.publish(coordinates)
     pub_life_of_hand.publish(life_of_hand_in_sensor)
     
     rate.sleep()
     
if __name__ == '__main__':
     try:
       leap_data()
     except rospy.ROSInterruptException:
       rospy.signal_shutdown("Programm being shutdown!")

