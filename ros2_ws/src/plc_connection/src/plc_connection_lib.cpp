#include "plc_connection/plc_connection.hpp"
#include "network/udp/udp_socket.hpp"
#include "network/socket/socket.hpp"
#include "rclcpp/rclcpp.hpp"
#include <cstdlib>
#include <memory>

// Konstruktor des Nodes
PlcConnectionNode::PlcConnectionNode()
: Node("PlcConnectionNode"),
ConnectionTimeout_(rclcpp::Duration::from_seconds(PLCTimeout_))
{
    seq_ = 0;

    // Erstelle einen Transform-Broadcaster
    TFBroadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

    // Parameter lesen, Socket initialisieren, Subscriber und Publisher erstellen
    ReadParams();
    InitializeSocket();
    Subscribe();
    CreatePublisher();

    // Erstelle einen Service zum Abrufen des Zählerstands
    CountServer_ = this->create_service<plc_connection::srv::GetCount>(
        "sensors/bodyAngle/getCounter", 
        std::bind(&PlcConnectionNode::GetCountService, this, std::placeholders::_1, std::placeholders::_2));
    
    // Erstelle einen Timer für das Senden und Empfangen von Daten
    SendRecvTimer_ = this->create_wall_timer(
        std::chrono::duration<double>(readWritePeriod_),
        std::bind(&PlcConnectionNode::SendRecv, this));

    // Initialisiere die Datenstruktur
    Data_.From.Speed[0] = 0;
    Data_.From.Speed[1] = 0;
    Data_.From.Speed[2] = 0;
    Data_.From.Speed[3] = 0;
    Data_.From.Angle = 0;

    Data_.To.Mode = 0;
    Data_.To.Speed[0] = 0;
    Data_.To.Speed[1] = 0;
    Data_.To.Speed[2] = 0;
    Data_.To.Speed[3] = 0;
    Data_.To.Dummy[0] = 0;
    Data_.To.Dummy[1] = 0;
    Data_.To.Dummy[2] = 0;
    Data_.To.Dummy[3] = 0;
}

// Destruktor des Nodes
PlcConnectionNode::~PlcConnectionNode() {}

// Initialisiert den UDP-Socket für die Kommunikation mit der PLC
void PlcConnectionNode::InitializeSocket()
{
    OwnUDP::Address tmpAddress;

    ConnectionTimeout_ = rclcpp::Duration::from_seconds(PLCTimeout_);
    RCLCPP_INFO(this->get_logger(), "PLC Timeout is set to %f seconds", PLCTimeout_);

    // Setze Zieladresse für die Kommunikation mit der PLC
    Target_.IP.IP = strTargetIP_;
    Target_.IP.Port = TargetPort_;
    RCLCPP_INFO(this->get_logger(), "PLC IP is %s:%i", strTargetIP_.c_str(), TargetPort_);

    Target_.LastID = 0;
    Target_.ComOk = false;
    Target_.LastMsgTime = this->get_clock()->now();

    tmpAddress.IP = strOwnIP_;
    tmpAddress.Port = OwnPort_;

    // Erstelle und konfiguriere den UDP-Socket
    RCLCPP_INFO(this->get_logger(), "Creating UDP Socket");
    try
    {
        PLC_Socket_.bindAddress(&tmpAddress);
        RCLCPP_INFO(this->get_logger(), "UDP Socket created on Port %i", OwnPort_);

        PLC_Socket_.setReceiveTime(ReceiveTimeoutUsec_, ReceiveTimeoutSec_);
        RCLCPP_INFO(this->get_logger(), "Receive Timeout for UDP Socket is set to %i seconds and %i usec", ReceiveTimeoutSec_, ReceiveTimeoutUsec_);
    }
    catch (const std::runtime_error& e)
    {
        RCLCPP_ERROR(this->get_logger(), "Error while creating UDP Socket on Port %i\n %s", OwnPort_, e.what());
        rclcpp::shutdown();
    }
}

// Liest die Parameter aus der ROS2-Parameterliste
void PlcConnectionNode::ReadParams()
{
    // Deklariere und initialisiere Parameter
    this->declare_parameter<std::string>("PLC_IP", "192.168.0.43");
    this->declare_parameter<std::string>("Xavier_IP", "");
    this->declare_parameter<int>("PLC_Port", 5000);
    this->declare_parameter<int>("Xavier_Port", 5000);
    this->declare_parameter<double>("PLC_Timeout", 1.5);
    this->declare_parameter<int>("Receive_Timeout_sec", 0);
    this->declare_parameter<int>("Receive_Timeout_usec", 500);
    this->declare_parameter<double>("Period_Send_Read", 0.05);
    this->declare_parameter<int>("ZeroCount_Encoder", 0);
    this->declare_parameter<float>("CountPerRotation_Encoder", 20000);
    this->declare_parameter<float>("Engine_Acceleration", 0);
    this->declare_parameter<float>("Engine_Jerk", 0);

    // Lese Parameter aus der Parameterliste
    this->get_parameter("PLC_IP", strTargetIP_);
    this->get_parameter("Xavier_IP", strOwnIP_);
    this->get_parameter("PLC_Port", TargetPort_);
    this->get_parameter("Xavier_Port", OwnPort_);
    this->get_parameter("PLC_Timeout", PLCTimeout_);
    this->get_parameter("Receive_Timeout_sec", ReceiveTimeoutSec_);
    this->get_parameter("Receive_Timeout_usec", ReceiveTimeoutUsec_);
    this->get_parameter("Period_Send_Read", readWritePeriod_);
    this->get_parameter("ZeroCount_Encoder", zeroCount_);
    this->get_parameter("CountPerRotation_Encoder", countPerRotation_);
    this->get_parameter("Engine_Acceleration", Data_.To.Accelleration);
    this->get_parameter("Engine_Jerk", Data_.To.Jerk);
    
    ConnectionTimeout_ = rclcpp::Duration::from_seconds(PLCTimeout_);
}

// Erstellt die Subscriber für Geschwindigkeit und Modus
void PlcConnectionNode::Subscribe()
{
    SpeedSubscriber_ = this->create_subscription<base::msg::Wheels>(
        "engine/targetSpeed", 1, std::bind(&PlcConnectionNode::SpeedCallback, this, std::placeholders::_1));

    ModeSubscriber_ = this->create_subscription<std_msgs::msg::UInt32>(
        "engine/mode", 1, std::bind(&PlcConnectionNode::ModeCallback, this, std::placeholders::_1));
}

// Erstellt die Publisher für Geschwindigkeit und Winkel
void PlcConnectionNode::CreatePublisher()
{
    SpeedPublisher_ = this->create_publisher<base::msg::Wheels>("engine/actualSpeed", 1);
    AnglePublisher_ = this->create_publisher<base::msg::Angle>("sensors/bodyAngle", 1);
}

// Callback-Funktion für den Geschwindigkeits-Subscriber
void PlcConnectionNode::SpeedCallback(const base::msg::Wheels::SharedPtr msg)
{
    Data_.To.Speed[0] = msg->front_right;
    Data_.To.Speed[1] = msg->front_left;
    Data_.To.Speed[2] = msg->rear_right;
    Data_.To.Speed[3] = msg->rear_left;
}

// Callback-Funktion für den Modus-Subscriber
void PlcConnectionNode::ModeCallback(const std_msgs::msg::UInt32::SharedPtr msg)
{
    Data_.To.Mode = msg->data;
}

// Service-Funktion zum Abrufen des Zählerstands
bool PlcConnectionNode::GetCountService(const std::shared_ptr<plc_connection::srv::GetCount::Request> request,
                        std::shared_ptr<plc_connection::srv::GetCount::Response> response)
{
    response->count = Data_.From.Angle;
    return true;
}

// Funktion zum Senden und Empfangen von Daten
void PlcConnectionNode::SendRecv()
{
    try
    {
        // Senden der Daten an die PLC
        SendData();

        // Empfangen der Daten von der PLC
        ReadData();
    }
    catch (std::runtime_error& e)
    {
        // Log the warning if necessary
    }
    
    // Veröffentlichen der empfangenen Daten
    PublishData();
}

// Funktion zum Senden von Daten an die PLC
void PlcConnectionNode::SendData()
{
    // Temporäre Datenstruktur für die Konvertierung
    PLC_Data tmpData;
    htonPLC(&tmpData, &Data_);

    // Senden der Daten über den UDP-Socket
    PLC_Socket_.write((uint8_t*)&tmpData.To, sizeof(Data_.To), &Target_.IP);
}

// Funktion zum Empfangen von Daten von der PLC
bool PlcConnectionNode::ReadData()
{
    // Temporäre Datenstruktur für die Konvertierung
    PLC_Data tmpData;
    OwnUDP::Address tmpAddress;

    // Lesen der Daten über den UDP-Socket
    PLC_Socket_.read((uint8_t*)&tmpData.From, sizeof(Data_.From), &tmpAddress);

    // Überprüfen, ob die empfangene Nachricht neu ist
    if (ntohl(tmpData.From.MessageID) == Target_.LastID)
    {
        // Überprüfen, ob die Verbindung zur PLC noch besteht
        if ((this->get_clock()->now() - Target_.LastMsgTime).seconds() > ConnectionTimeout_.seconds())
        {
            if (Target_.ComOk == true)
            {
                RCLCPP_ERROR(this->get_logger(), "No Connection to PLC");
            }
            Target_.ComOk = false;
        }
        return false;
    }

    // Konvertiere die empfangenen Daten in das Host-Format
    ntohPLC(&Data_, &tmpData);

    // Aktualisiere den Verbindungsstatus zur PLC
    Target_.ComOk = true;
    Target_.LastID = Data_.From.MessageID;
    Target_.LastMsgTime = this->get_clock()->now();

    return true;
}

// Funktion zum Veröffentlichen der empfangenen Daten
void PlcConnectionNode::PublishData()
{
    // Nachrichtenstrukturen für die Veröffentlichung der Daten
    base::msg::Angle AngleMsg;
    base::msg::Wheels SpeedMsg;
    geometry_msgs::msg::TransformStamped TfAngleMsg;
    tf2::Quaternion q;

    // Berechne den Winkel in Radiant basierend auf dem Zählerstand und der Zählung pro Umdrehung
    float Angle = (((float)Data_.From.Angle - (float)zeroCount_) / countPerRotation_) * 2 * M_PI;

    // Setze die Zeitstempel und IDs für die Transformationsnachrich
    TfAngleMsg.header.stamp = this->get_clock()->now();
    TfAngleMsg.child_frame_id = "jointRear";
    TfAngleMsg.header.frame_id = "jointFront";

    // Setze die Zeitstempel für die Geschwindigkeits- und Winkel-Nachrichten
    SpeedMsg.header.stamp = this->get_clock()->now();
    AngleMsg.header.stamp = this->get_clock()->now();

    // Setze die Transformation basierend auf dem berechneten Winkel
    q.setRPY(0, 0, Angle);
    TfAngleMsg.transform.translation.x = 0;
    TfAngleMsg.transform.translation.y = 0;
    TfAngleMsg.transform.translation.z = 0;
    TfAngleMsg.transform.rotation.x = q.x();
    TfAngleMsg.transform.rotation.y = q.y();
    TfAngleMsg.transform.rotation.z = q.z();
    TfAngleMsg.transform.rotation.w = q.w();

    // Setze die empfangenen Geschwindigkeitswerte in die Nachricht
    SpeedMsg.front_right = Data_.From.Speed[0];
    SpeedMsg.front_left = Data_.From.Speed[1];
    SpeedMsg.rear_right = Data_.From.Speed[2];
    SpeedMsg.rear_left = Data_.From.Speed[3];

    // Setze den berechneten Winkel in die Nachricht
    AngleMsg.angle = Angle;

    // Sende die Transformationsnachricht
    TFBroadcaster_->sendTransform(TfAngleMsg);

    // Veröffentliche die Geschwindigkeits- und Winkel-Nachrichten
    SpeedPublisher_->publish(SpeedMsg);
    AnglePublisher_->publish(AngleMsg);
}

// Funktion zum Konvertieren von Netzwerk- zu Host-Daten
void ntohPLC(PLC_Data* Host, PLC_Data* Network)
{
    Host->From.MessageID = ntohl(Network->From.MessageID);
    Host->From.Mode = ntohl(Network->From.Mode);
    Host->From.Angle = ntohl(Network->From.Angle);
    Host->From.Voltage = OwnSocket::ntohf(Network->From.Voltage);
    Host->From.HomingError = ntohl(Network->From.HomingError);
    Host->From.Angle_rad = OwnSocket::ntohf(Network->From.Angle_rad);

    for (int i = 0; i < 4; i++)
    {
        Host->From.Speed[i] = OwnSocket::ntohf(Network->From.Speed[i]);
        Host->From.SpeedError[i] = ntohl(Network->From.SpeedError[i]);
        Host->From.ResetError[i] = ntohl(Network->From.ResetError[i]);
    }
}

// Funktion zum Konvertieren von Host- zu Netzwerk-Daten
void htonPLC(PLC_Data* Network, PLC_Data* Host)
{
    Network->To.MessageID = htonl(Host->To.MessageID++);
    Network->To.Mode = htonl(Host->To.Mode);
    Network->To.Jerk = OwnSocket::htonf(Host->To.Jerk);
    Network->To.Accelleration = OwnSocket::htonf(Host->To.Accelleration);

    for (int i = 0; i < 4; i++)
    {
        Network->To.Speed[i] = OwnSocket::htonf(Host->To.Speed[i]);
        Network->To.Dummy[i] = OwnSocket::htonf(Host->To.Dummy[i]);
    }
}