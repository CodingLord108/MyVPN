import socket

def start_local_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen(5)
    print("Local Server listening on port 9090...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        try:
            while True:
                data = client_socket.recv(1024)
                if data:
                    received_message = data.decode()
                    print("Received from VPN Server:", received_message)

                    # If the message is "bye", send a farewell and close the server
                    if received_message.lower() == "bye":
                        farewell_message = "Goodbye! Closing connection."
                        client_socket.send(farewell_message.encode())
                        print("Ending conversation.")
                        return  # Exit the local server

                    # Prompt the operator to enter a custom response
                    response = input("Enter response to client: ")
                    client_socket.send(response.encode())
                else:
                    break
        finally:
            client_socket.close()

start_local_server()
