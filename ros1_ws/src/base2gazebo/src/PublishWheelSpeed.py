import rospy
from base2gazebo.msg import Wheels
from std_msgs.msg import Float64

def callback(data):
    pub = rospy.Publisher('/gazebo/joint_fl_controller/command', Float64, queue_size=10)
    pub.publish(data.front_left)
    pub = rospy.Publisher('/gazebo/joint_fr_controller/command', Float64, queue_size=10)
    pub.publish(data.front_right)
    pub = rospy.Publisher('/gazebo/joint_rl_controller/command', Float64, queue_size=10)
    pub.publish(data.rear_left)
    pub = rospy.Publisher('/gazebo/joint_rr_controller/command', Float64, queue_size=10)
    pub.publish(data.rear_right)

    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/engine/targetSpeed", Wheels, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
