
(cl:in-package :asdf)

(defsystem "base-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Angle" :depends-on ("_package_Angle"))
    (:file "_package_Angle" :depends-on ("_package"))
    (:file "Wheels" :depends-on ("_package_Wheels"))
    (:file "_package_Wheels" :depends-on ("_package"))
  ))