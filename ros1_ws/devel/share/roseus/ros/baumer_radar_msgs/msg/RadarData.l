;; Auto-generated. Do not edit!


(when (boundp 'baumer_radar_msgs::RadarData)
  (if (not (find-package "BAUMER_RADAR_MSGS"))
    (make-package "BAUMER_RADAR_MSGS"))
  (shadow 'RadarData (find-package "BAUMER_RADAR_MSGS")))
(unless (find-package "BAUMER_RADAR_MSGS::RADARDATA")
  (make-package "BAUMER_RADAR_MSGS::RADARDATA"))

(in-package "ROS")
;;//! \htmlinclude RadarData.msg.html


(defclass baumer_radar_msgs::RadarData
  :super ros::object
  :slots (_status _confidence _distance _reserved _velocity ))

(defmethod baumer_radar_msgs::RadarData
  (:init
   (&key
    ((:status __status) 0)
    ((:confidence __confidence) 0)
    ((:distance __distance) 0.0)
    ((:reserved __reserved) "")
    ((:velocity __velocity) 0.0)
    )
   (send-super :init)
   (setq _status (round __status))
   (setq _confidence (round __confidence))
   (setq _distance (float __distance))
   (setq _reserved (string __reserved))
   (setq _velocity (float __velocity))
   self)
  (:status
   (&optional __status)
   (if __status (setq _status __status)) _status)
  (:confidence
   (&optional __confidence)
   (if __confidence (setq _confidence __confidence)) _confidence)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:reserved
   (&optional __reserved)
   (if __reserved (setq _reserved __reserved)) _reserved)
  (:velocity
   (&optional __velocity)
   (if __velocity (setq _velocity __velocity)) _velocity)
  (:serialization-length
   ()
   (+
    ;; int32 _status
    4
    ;; int32 _confidence
    4
    ;; float32 _distance
    4
    ;; string _reserved
    4 (length _reserved)
    ;; float32 _velocity
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _status
       (write-long _status s)
     ;; int32 _confidence
       (write-long _confidence s)
     ;; float32 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; string _reserved
       (write-long (length _reserved) s) (princ _reserved s)
     ;; float32 _velocity
       (sys::poke _velocity (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _status
     (setq _status (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _confidence
     (setq _confidence (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _distance
     (setq _distance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; string _reserved
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _reserved (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _velocity
     (setq _velocity (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get baumer_radar_msgs::RadarData :md5sum-) "39955ca1f98a7669eaa59409eac1a196")
(setf (get baumer_radar_msgs::RadarData :datatype-) "baumer_radar_msgs/RadarData")
(setf (get baumer_radar_msgs::RadarData :definition-)
      "int32 status
int32 confidence
float32 distance
string reserved
float32 velocity

")



(provide :baumer_radar_msgs/RadarData "39955ca1f98a7669eaa59409eac1a196")


