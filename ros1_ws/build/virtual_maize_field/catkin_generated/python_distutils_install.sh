#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/jannis/flori2/ros1_ws/src/virtual_maize_field"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/jannis/flori2/ros1_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/jannis/flori2/ros1_ws/install/lib/python3/dist-packages:/home/jannis/flori2/ros1_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/jannis/flori2/ros1_ws/build" \
    "/usr/bin/python3" \
    "/home/jannis/flori2/ros1_ws/src/virtual_maize_field/setup.py" \
     \
    build --build-base "/home/jannis/flori2/ros1_ws/build/virtual_maize_field" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/jannis/flori2/ros1_ws/install" --install-scripts="/home/jannis/flori2/ros1_ws/install/bin"
