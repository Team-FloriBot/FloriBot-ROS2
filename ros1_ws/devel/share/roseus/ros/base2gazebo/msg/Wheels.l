;; Auto-generated. Do not edit!


(when (boundp 'base2gazebo::Wheels)
  (if (not (find-package "BASE2GAZEBO"))
    (make-package "BASE2GAZEBO"))
  (shadow 'Wheels (find-package "BASE2GAZEBO")))
(unless (find-package "BASE2GAZEBO::WHEELS")
  (make-package "BASE2GAZEBO::WHEELS"))

(in-package "ROS")
;;//! \htmlinclude Wheels.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass base2gazebo::Wheels
  :super ros::object
  :slots (_header _frontLeft _frontRight _rearLeft _rearRight ))

(defmethod base2gazebo::Wheels
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:frontLeft __frontLeft) 0.0)
    ((:frontRight __frontRight) 0.0)
    ((:rearLeft __rearLeft) 0.0)
    ((:rearRight __rearRight) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _frontLeft (float __frontLeft))
   (setq _frontRight (float __frontRight))
   (setq _rearLeft (float __rearLeft))
   (setq _rearRight (float __rearRight))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:frontLeft
   (&optional __frontLeft)
   (if __frontLeft (setq _frontLeft __frontLeft)) _frontLeft)
  (:frontRight
   (&optional __frontRight)
   (if __frontRight (setq _frontRight __frontRight)) _frontRight)
  (:rearLeft
   (&optional __rearLeft)
   (if __rearLeft (setq _rearLeft __rearLeft)) _rearLeft)
  (:rearRight
   (&optional __rearRight)
   (if __rearRight (setq _rearRight __rearRight)) _rearRight)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _frontLeft
    8
    ;; float64 _frontRight
    8
    ;; float64 _rearLeft
    8
    ;; float64 _rearRight
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _frontLeft
       (sys::poke _frontLeft (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _frontRight
       (sys::poke _frontRight (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rearLeft
       (sys::poke _rearLeft (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rearRight
       (sys::poke _rearRight (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _frontLeft
     (setq _frontLeft (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _frontRight
     (setq _frontRight (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rearLeft
     (setq _rearLeft (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rearRight
     (setq _rearRight (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get base2gazebo::Wheels :md5sum-) "88a446f832904937708e487c974640d3")
(setf (get base2gazebo::Wheels :datatype-) "base2gazebo/Wheels")
(setf (get base2gazebo::Wheels :definition-)
      "Header header
float64 frontLeft
float64 frontRight
float64 rearLeft
float64 rearRight
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :base2gazebo/Wheels "88a446f832904937708e487c974640d3")

