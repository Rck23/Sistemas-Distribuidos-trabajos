import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Servidor Centralizado 
class ServerGUI:
    def __init__(self, host="127.0.0.1", port=5000):
        self.server_ip = host
        self.server_port = port
        self.clients = [  # Lista para almacenar IPs y Puertos 
            ("127.0.0.1", 6001),
            ("127.0.0.1", 6002),
            ("127.0.0.1", 6003)
        ]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.server_ip, self.server_port))
        print(f"Servidor escuchando en {self.server_ip}:{self.server_port}")

        # Interfaz gráfica del servidor
        self.window = tk.Tk()
        self.window.title("Servidor Centralizado")

        self.text_area = scrolledtext.ScrolledText(self.window, width=50, height=20, state='disabled')
        self.text_area.pack(padx=10, pady=10)

        self.entry_frame = tk.Frame(self.window)
        self.entry_frame.pack(pady=(0, 10))

        self.entry_message = tk.Entry(self.entry_frame, width=40)
        self.entry_message.pack(side=tk.LEFT, padx=(10, 5))

        self.send_button = tk.Button(self.entry_frame, text="Enviar a Todos", command=self.send_message, bg="lightblue", fg="black")
        self.send_button.pack(side=tk.LEFT, padx=(5, 10))

        threading.Thread(target=self.start, daemon=True).start()

        self.window.mainloop()

    def start(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()

            if message.startswith("REGISTRO:"):
                # Registrar un nuevo nodo cliente
                _, client_port = message.split(":")
                self.clients.append((addr[0], int(client_port)))
                self.display_message(f"Nodo registrado: {addr[0]}:{client_port}")
            else:
                # Reenviar el mensaje a todos los nodos registrados
                self.display_message(f"Mensaje recibido de {addr}: {message}")
                self.broadcast(message, addr)

    def broadcast(self, message, sender_addr=None):
        for client in self.clients:
            if client != sender_addr: 
                self.sock.sendto(message.encode(), client)

    def send_message(self):
        message = self.entry_message.get()
        if message:
            self.broadcast(message)  
            self.display_message(f"Servidor: {message}")
            self.entry_message.delete(0, tk.END)

    def display_message(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)


class ClientGUI:
    def __init__(self, server_ip="127.0.0.1", server_port=5000, listen_port=0):
        self.server_ip = server_ip
        self.server_port = server_port
        self.listen_port = listen_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", self.listen_port))  # Escucha en el puerto definido
        self.listen_port = self.sock.getsockname()[1]  # Obtener el puerto real 

        self.sock.sendto(f"REGISTRO:{self.listen_port}".encode(), (self.server_ip, self.server_port))

        # Configurar la interfaz gráfica
        self.window = tk.Tk()
        self.window.title(f"Cliente P2P - Puerto {self.listen_port}")

        self.text_area = scrolledtext.ScrolledText(self.window, width=50, height=20, state='disabled')
        self.text_area.pack(padx=10, pady=10)

        self.entry_frame = tk.Frame(self.window)
        self.entry_frame.pack(pady=(0, 10))

        self.entry_message = tk.Entry(self.entry_frame, width=40)
        self.entry_message.pack(side=tk.LEFT, padx=(10, 5))

        self.send_button = tk.Button(self.entry_frame, text="Enviar", command=self.send_message, bg="lightgreen", fg="black")
        self.send_button.pack(side=tk.LEFT, padx=(5, 10))

        # Hilo para escuchar mensajes entrantes
        threading.Thread(target=self.listen, daemon=True).start()

        self.window.mainloop()

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = f"{addr[0]}:{addr[1]} dice: {data.decode()}"
            self.display_message(message)

    def send_message(self):
        message = self.entry_message.get()
        if message:
            self.sock.sendto(message.encode(), (self.server_ip, self.server_port))
            self.display_message(f"Tú: {message}")
            self.entry_message.delete(0, tk.END)

    def display_message(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "server":
        ServerGUI()
    else:
        listen_port = int(input("Puerto de escucha del cliente: "))
        ClientGUI(listen_port=listen_port)
