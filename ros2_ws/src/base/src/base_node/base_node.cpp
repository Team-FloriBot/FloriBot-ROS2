#include "base_node/base_publisher.hpp"  // Stellen sicher, dass der Pfad stimmt

void ExitFcn();

int main(int argc, char** argv)
{
    // ROS2 initialisieren
    rclcpp::init(argc, argv);

    // ROS2-Node erstellen
    try
    {
        // Ein Knotenobjekt erstellen
        rclcpp::NodeOptions options;
        auto node = std::make_shared<rclcpp::Node>("Kinematics", options);

        // KinematicsPublisher mit dem Knoten erstellen
        KinematicsPublisher Pub(node, kinematics::coordinate::Front);

        // ROS2 spinnt den Knoten
        rclcpp::spin(node);
    }
    catch(const std::runtime_error& e)
    {
        // Fehlerbehandlung in ROS2
        RCLCPP_ERROR(rclcpp::get_logger("Kinematics"), "Exiting with error:\n%s\n", e.what());
        return 1; // Exit mit Fehlercode
    }

    // Aufräumarbeiten bei normalem Abschluss
    rclcpp::shutdown();
    return 0;
}

void ExitFcn()
{
    RCLCPP_ERROR(rclcpp::get_logger("Kinematics"), "Exiting Node: %s \n", rclcpp::get_node_name().c_str());
}

