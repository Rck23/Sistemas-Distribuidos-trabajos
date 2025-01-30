# Código del Cliente
import socket

def cliente_tcp(ip, puerto):
    # Crear el socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"[CLIENTE] Conectando a {ip}:{puerto}...")
        cliente.connect((ip, puerto))
        print("[CLIENTE] Conexión exitosa.")

        # Enviar el mensaje
        mensaje = "¡¡¡HOLA MUNDO!!!"
        cliente.sendall(mensaje.encode('utf-8'))
        print(f"[CLIENTE] Mensaje enviado: {mensaje}")
    except Exception as e:
        print(f"[CLIENTE] Error: {e}")
    finally:
        cliente.close()
        print("[CLIENTE] Conexión cerrada.")

ip_cliente = "127.0.0.1"
puerto_cliente = 10001
cliente_tcp(ip_cliente, puerto_cliente)
