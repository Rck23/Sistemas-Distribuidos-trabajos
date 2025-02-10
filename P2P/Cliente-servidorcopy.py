import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuración de red
LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 12346
DEST_IP = "127.0.0.1"
DEST_PORT = 12345


# Función del servidor
def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LOCAL_IP, LOCAL_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data:
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"Recibido: {data.decode()}\n")
                chat_box.config(state=tk.DISABLED)
        except:
            break


# Función para enviar mensajes
def send_message():
    message = message_entry.get()
    if message:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), (DEST_IP, DEST_PORT))
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"Enviado: {message}\n")
        chat_box.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)


# Interfaz gráfica
root = tk.Tk()
root.title("P2P copy")

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=20)
chat_box.pack()

message_entry = tk.Entry(root, width=50)
message_entry.pack()

send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack()

# Iniciar el servidor en un hilo
threading.Thread(target=server, daemon=True).start()

# Ejecutar la interfaz gráfica
root.mainloop()
