import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

LOCAL_SERVER_PORT = 9090

class LocalServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Server")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)
        self.text_area.insert(tk.END, "Local Server listening on port 9090...\n")

        self.entry = tk.Entry(root, width=40)
        self.entry.grid(column=0, row=1, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_response)
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', LOCAL_SERVER_PORT))  # Set to localhost
        self.server_socket.listen(5)

        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while True:
            self.client_socket, addr = self.server_socket.accept()
            self.text_area.insert(tk.END, f"Connection established with {addr}\n")
            threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    message = data.decode()
                    self.text_area.insert(tk.END, f"VPN Server: {message}\n")
                    if message.lower() == "bye":
                        self.text_area.insert(tk.END, "Ending conversation.\n")
                        break
            except ConnectionResetError:
                break

    def send_response(self, event=None):
        response = self.entry.get()
        self.text_area.insert(tk.END, f"Local Server: {response}\n")
        self.client_socket.send(response.encode())
        self.entry.delete(0, tk.END)

root = tk.Tk()
app = LocalServerApp(root)
root.mainloop()
