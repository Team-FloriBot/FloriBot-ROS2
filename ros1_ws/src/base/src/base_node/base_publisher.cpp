#include <base_node/base_publisher.h>

KinematicsPublisher::KinematicsPublisher(ros::NodeHandle* pNh, kinematics::coordinate Base)
{
    seq_=0;
    pNh_=pNh;
    getParam();
    Drive_.setParam(AxesLength_, WheelDiameter_, Base);
    createPublisherSubscriber();
    CmdVelTimer_=pNh_->createTimer(ros::Duration(0.1), &KinematicsPublisher::PublishSpeed, this);
}
KinematicsPublisher::~KinematicsPublisher(){};

void KinematicsPublisher::PublishSpeed(const ros::TimerEvent& e)
{
    base::Wheels tmp;

    tmp.header.stamp=ros::Time::now();
    tmp.header.seq=seq_++;
    tmp.frontLeft=Speedmsg_.front_left;
    tmp.frontRight=Speedmsg_.front_right;
    tmp.rearLeft=Speedmsg_.rear_left;
    tmp.rearLeft=Speedmsg_.rear_right;


    SpeedPublisher_.publish(Speedmsg_);

    Speedmsg_.front_left=0;
    Speedmsg_.front_right=0;    
    Speedmsg_.rear_right=0;
    Speedmsg_.rear_left=0;
}

void KinematicsPublisher::getParam()
{
    pNh_->param<double>("/"+ros::this_node::getName()+"/axesLength", AxesLength_, 0.4);
    pNh_->param<double>("/"+ros::this_node::getName()+"/wheelDiameter", WheelDiameter_, 0.4);
}

void KinematicsPublisher::createPublisherSubscriber()
{
    OdometryPublisher_=pNh_->advertise<nav_msgs::Odometry>("/odom", 1);
    SpeedPublisher_=pNh_->advertise<base::Wheels>("engine/targetSpeed", 1);

    CmdVelSubscriber_=pNh_->subscribe("cmd_vel", 1, &KinematicsPublisher::CmdVelCallback, this);
    SpeedSubscriber_=pNh_->subscribe("engine/actualSpeed", 1, &KinematicsPublisher::SpeedCallback, this);    
}

void KinematicsPublisher::CmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
    kinematics::articulatedWheelSpeed Wheelspeed;

    Wheelspeed=Drive_.inverseKinematics(*msg);

    Speedmsg_.front_left=Wheelspeed.Front.leftWheel;
    Speedmsg_.front_right=Wheelspeed.Front.rightWheel;

    Speedmsg_.rear_left=Wheelspeed.Rear.leftWheel;
    Speedmsg_.rear_right=Wheelspeed.Rear.rightWheel;
}

void KinematicsPublisher::SpeedCallback(const base::Wheels::ConstPtr &msg)
{
    kinematics::articulatedWheelSpeed ActualSpeed;
    geometry_msgs::Pose2D OdomPose;
    geometry_msgs::TransformStamped Transform;
    nav_msgs::Odometry OdomMsg;
    tf2::Quaternion q;

    ActualSpeed.Front.leftWheel=msg->front_left;
    ActualSpeed.Front.rightWheel=msg->front_right;
    ActualSpeed.Rear.leftWheel=msg->rear_left;
    ActualSpeed.Rear.rightWheel=msg->rear_right;

    OdomPose=Drive_.forwardKinematics(ActualSpeed, msg->header.stamp );

     
    //Front Msg
    q.setRPY(0, 0, OdomPose.theta);

    //TF Msg
    Transform.child_frame_id="base_link";
    Transform.header.frame_id="odom";
    Transform.header.seq=msg->header.seq;
    Transform.header.stamp=msg->header.stamp;

    Transform.transform.translation.x=OdomPose.x;
    Transform.transform.translation.y=OdomPose.y;
    Transform.transform.translation.z=WheelDiameter_/2;

    Transform.transform.rotation.w=q.getW();
    Transform.transform.rotation.x=q.getX();
    Transform.transform.rotation.y=q.getY();
    Transform.transform.rotation.z=q.getZ();
   
    //ToDo: Add Covariance
    //Odom Msg
    OdomMsg.child_frame_id="base_link";
    OdomMsg.header.frame_id="odom";
    OdomMsg.header.seq=msg->header.seq;
    OdomMsg.header.stamp=msg->header.stamp;

    OdomMsg.pose.pose.orientation.w=q.getW();
    OdomMsg.pose.pose.orientation.x=q.getX();
    OdomMsg.pose.pose.orientation.y=q.getY();
    OdomMsg.pose.pose.orientation.z=q.getZ();

    OdomMsg.pose.pose.position.x=OdomPose.x;
    OdomMsg.pose.pose.position.y=OdomPose.y;
    OdomMsg.pose.pose.position.z=WheelDiameter_/2;


    //According to http://wiki.ros.org/navigation/Tutorials/RobotSetup/Odom the speed has to be in the child_frame
    //in our case base_link which means the robot itself

    OdomMsg.twist.twist=Drive_.getSpeed();    

    //publish
    OdometryPublisher_.publish(OdomMsg);

    TFBroadaster_.sendTransform(Transform);

}