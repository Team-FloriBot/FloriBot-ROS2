
(cl:in-package :asdf)

(defsystem "baumer_radar_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "RadarData" :depends-on ("_package_RadarData"))
    (:file "_package_RadarData" :depends-on ("_package"))
  ))