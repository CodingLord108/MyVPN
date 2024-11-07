import socket
import ssl

def start_vpn_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # For testing purposes

    secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")
    secure_socket.connect(('localhost', 8080))
    print("Connected to VPN Server")

    try:
        while True:
            message = input("Client: ")
            secure_socket.send(message.encode())

            # Check if the message is "bye" to end the conversation
            if message.lower() == "bye":
                data = secure_socket.recv(1024)
                print("Response from server:", data.decode())
                print("Ending conversation.")
                break

            data = secure_socket.recv(1024)
            print("Response from server:", data.decode())
    finally:
        secure_socket.close()

start_vpn_client()
