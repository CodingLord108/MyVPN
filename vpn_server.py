import socket
import ssl

# VPN Server settings
VPN_HOST = 'localhost'
VPN_PORT = 8080

# Local Server settings
LOCAL_SERVER_HOST = 'localhost'
LOCAL_SERVER_PORT = 9090

def forward_to_local_server(data):
    # Connect to the local server to forward the data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as local_server_socket:
        local_server_socket.connect((LOCAL_SERVER_HOST, LOCAL_SERVER_PORT))
        local_server_socket.sendall(data)
        # Receive the response from the local server
        response = local_server_socket.recv(1024)
        return response

def start_vpn_server():
    # Set up a TCP socket and wrap it with SSL for encryption
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((VPN_HOST, VPN_PORT))
    server_socket.listen(5)

    # SSL context for secure connection
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

    print(f"VPN Server listening on {VPN_HOST}:{VPN_PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)
        print(f"Connection established with {addr}")

        try:
            while True:
                # Receive data from VPN Client
                data = secure_socket.recv(1024)
                if data:
                    print("Received from client:", data.decode())

                    # Check if the message is "bye" to terminate the connection
                    if data.decode().lower() == "bye":
                        response = forward_to_local_server(data)
                        print("Response from Local Server:", response.decode())  # Show response in VPN server
                        secure_socket.send(response)
                        print("Ending conversation.")
                        return  # Exit the VPN server

                    # Forward to Local Server
                    response = forward_to_local_server(data)
                    # Display the response from Local Server
                    print("Response from Local Server:", response.decode())
                    # Send the Local Server's response back to the VPN Client
                    secure_socket.send(response)
                else:
                    break
        finally:
            secure_socket.close()

start_vpn_server()
