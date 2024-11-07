import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext

VPN_SERVER_HOST = '127.0.0.1'  # Set to localhost for testing
VPN_SERVER_PORT = 8080

class VPNClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VPN Client")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.grid(column=0, row=1, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        self.secure_socket = self.context.wrap_socket(self.client_socket, server_hostname=VPN_SERVER_HOST)
        self.secure_socket.connect((VPN_SERVER_HOST, VPN_SERVER_PORT))
        self.text_area.insert(tk.END, "Connected to VPN Server\n")

    def send_message(self, event=None):
        message = self.entry.get()
        self.text_area.insert(tk.END, f"Client: {message}\n")
        self.secure_socket.send(message.encode())
        self.entry.delete(0, tk.END)

        if message.lower() == "bye":
            self.text_area.insert(tk.END, "Ending conversation.\n")
            self.root.quit()  # Close the GUI

        # Receive the server's response
        data = self.secure_socket.recv(1024)
        if data:
            self.text_area.insert(tk.END, f"Response from server: {data.decode()}\n")

root = tk.Tk()
app = VPNClientApp(root)
root.mainloop()
