execute_process(COMMAND "/home/jannis/flori2/ros1_ws/build/virtual_maize_field/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/jannis/flori2/ros1_ws/build/virtual_maize_field/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
