import socket
import threading
import tkinter as tk
from tkinter import messagebox

class GatoP2P:
    def __init__(self, host, port, peer_host, peer_port):
        self.host = host
        self.port = port
        self.peer_host = peer_host
        self.peer_port = peer_port
        self.board = ["" for _ in range(9)]
        self.current_turn = True  # True si es el turno del jugador local

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe P2P " + f"{self.peer_port}")
        self.buttons = [tk.Button(self.window, text="", font=("Arial", 24), width=5, height=2,
                                  command=lambda i=i: self.make_move(i)) for i in range(9)]

        for i in range(3):
            for j in range(3):
                self.buttons[i * 3 + j].grid(row=i, column=j)

        self.status_label = tk.Label(self.window, text="Tu turno", font=("Arial", 14))
        self.status_label.grid(row=3, column=0, columnspan=3)

        threading.Thread(target=self.listen_for_moves, daemon=True).start()
        self.window.mainloop()

    def make_move(self, index):
        if self.board[index] == "" and self.current_turn:
            self.board[index] = "X"
            self.buttons[index].config(text="X", state=tk.DISABLED)
            self.current_turn = False
            self.status_label.config(text="Turno del oponente")
            self.sock.sendto(str(index).encode(), (self.peer_host, self.peer_port))
            self.check_winner()

    def receive_move(self, index):
        self.board[index] = "O"
        self.buttons[index].config(text="O", state=tk.DISABLED)
        self.current_turn = True
        self.status_label.config(text="Tu turno")
        self.check_winner()

    def listen_for_moves(self):
        while True:
            data, _ = self.sock.recvfrom(1024)
            index = int(data.decode())
            self.receive_move(index)

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                winner = "Tú" if self.board[a] == "X" else "Tu oponente"
                messagebox.showinfo("Juego terminado", f"{winner} ha ganado!")
                self.window.quit()
                return
        if "" not in self.board:
            messagebox.showinfo("Juego terminado", "Empate!")
            self.window.quit()


if __name__ == "__main__":
    host = input("Ingresa tu IP: ")
    port = int(input("Ingresa tu puerto: "))
    peer_host = input("Ingresa la IP del oponente: ")
    peer_port = int(input("Ingresa el puerto del oponente: "))
    GatoP2P(host, port, peer_host, peer_port)




"""
Un juego de Gato (Tic-Tac-Toe) peer-to-peer usando Tkinter para la GUI y sockets UDP para la comunicación.
Atributos:
    host (str): La dirección IP del host local.
    port (int): El número de puerto local.
    peer_host (str): La dirección IP del host del oponente.
    peer_port (int): El número de puerto del oponente.
    board (list): El tablero de Tic-Tac-Toe representado como una lista de cadenas.
    current_turn (bool): True si es el turno del jugador local, False en caso contrario.
    sock (socket.socket): El socket UDP para la comunicación.
    window (tk.Tk): La ventana principal de Tkinter.
    buttons (list): Lista de botones de Tkinter que representan el tablero de Tic-Tac-Toe.
    status_label (tk.Label): Etiqueta para mostrar el estado actual del juego.
Métodos:
    __init__(host, port, peer_host, peer_port):
        Inicializa la instancia de GatoP2P y configura la GUI y el socket.
    make_move(index):
        Maneja el movimiento del jugador local y lo envía al oponente.
    receive_move(index):
        Maneja el movimiento del oponente y actualiza el tablero.
    listen_for_moves():
        Escucha los movimientos entrantes del oponente.
    check_winner():
        Verifica si hay un ganador o si el juego es un empate.
"""