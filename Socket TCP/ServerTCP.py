# Código del Servidor
import socket

def servidor_tcp(ip, puerto):
    # Crear el socket
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, puerto))
    servidor.listen(1)  # Escuchar conexiones entrantes
    print(f"[SERVIDOR] Escuchando en {ip}:{puerto}...")

    while True:
        print("[SERVIDOR] Esperando conexión...")
        conexion, direccion = servidor.accept()
        print(f"[SERVIDOR] Conexión establecida con {direccion}")

        mensaje = conexion.recv(1024).decode('utf-8')
        print(f"[SERVIDOR] Mensaje recibido: {mensaje}")

        conexion.close()
        print("[SERVIDOR] Conexión cerrada.")

# Cambia la IP y el puerto según sea necesario
ip_servidor = "127.0.0.1"
puerto_servidor = 10001
servidor_tcp(ip_servidor, puerto_servidor)
