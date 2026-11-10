import os
import socket
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("TCP_HOST", "127.0.0.1")
PORTA = int(os.getenv("TCP_PORT", "5050"))


def testarServidor():
    #Utilizei um cliente separado para demonstrar o envio e o recebimento de dados via TCP
    with socket.create_connection((HOST, PORTA), timeout=5) as cliente:
        cliente.sendall("PING\n".encode("utf-8"))
        resposta = cliente.recv(1024).decode("utf-8")
        print("Resposta do servidor:", resposta)


if __name__ == "__main__":
    try:
        testarServidor()
    except OSError:
        print("Não foi possível conectar. Verifique se o servidor TCP está iniciado.")
