import os
import socket
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("TCP_HOST", "127.0.0.1")
PORTA = int(os.getenv("TCP_PORT", "5050"))


def iniciarServidor():
    #Utilizei TCP porque ele estabelece uma conexão confiável para o teste simples de comunicação.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen(5)
        print(f"Servidor BEalive aguardando em {HOST}:{PORTA}")
        while True:
            conexao, endereco = servidor.accept()
            with conexao:
                mensagem = conexao.recv(1024).decode("utf-8").strip()
                if mensagem == "PING":
                    conexao.sendall("BEalive ativo".encode("utf-8"))
                else:
                    conexao.sendall("Comando inválido".encode("utf-8"))


if __name__ == "__main__":
    iniciarServidor()
