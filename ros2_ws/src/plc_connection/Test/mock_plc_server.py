import socket
import struct
import time

def start_mock_plc_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"Mock PLC server started on {ip}:{port}")

    message_id = 0

    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received message from {addr}: {data}")

            # Increment message ID for each new message
            message_id += 1

            # Prepare a response with the expected data structure
            response = struct.pack(
                '!IIf4f4I',
                message_id,              # MessageID
                1,                       # Mode
                12345,                   # Angle
                12.34, 56.78, 90.12, 34.56, # Speed[4]
                0, 0, 0, 0               # SpeedError[4]
            )

            server_socket.sendto(response, addr)
            time.sleep(0.5)  # Send messages at regular intervals
    except KeyboardInterrupt:
        print("Mock PLC server shutting down")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_mock_plc_server("127.0.0.1", 50001)