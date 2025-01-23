
(cl:in-package :asdf)

(defsystem "base2gazebo-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Wheels" :depends-on ("_package_Wheels"))
    (:file "_package_Wheels" :depends-on ("_package"))
  ))