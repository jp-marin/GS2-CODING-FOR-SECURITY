import os
import mysql.connector
from dotenv import load_dotenv

#Utilizei dotenv para manter as credenciais fora dos arquivos versionados
load_dotenv()


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "bealive")
    )
