import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext

VPN_SERVER_PORT = 8080
LOCAL_SERVER_HOST = '127.0.0.1'  # Set to localhost for testing
LOCAL_SERVER_PORT = 9090

class VPNServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VPN Server")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)
        self.text_area.insert(tk.END, "VPN Server listening on port 8080...\n")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', VPN_SERVER_PORT))  # Set to localhost
        self.server_socket.listen(5)

        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.secure_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
            self.text_area.insert(tk.END, f"Connected with {addr}\n")
            threading.Thread(target=self.handle_client).start()

    def handle_client(self):
        while True:
            try:
                data = self.secure_socket.recv(1024)
                if data:
                    message = data.decode()
                    self.text_area.insert(tk.END, f"Client: {message}\n")
                    response = self.forward_to_local_server(data)
                    self.secure_socket.send(response)
            except ConnectionResetError:
                break

    def forward_to_local_server(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as local_socket:
            local_socket.connect((LOCAL_SERVER_HOST, LOCAL_SERVER_PORT))
            local_socket.sendall(data)
            response = local_socket.recv(1024)
            self.text_area.insert(tk.END, f"Local Server Response: {response.decode()}\n")
            return response

root = tk.Tk()
app = VPNServerApp(root)
root.mainloop()
