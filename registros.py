import logging
from pathlib import Path

pastaLogs = Path(__file__).resolve().parent / "logs"
pastaLogs.mkdir(exist_ok=True)
arquivoLog = pastaLogs / "bealive.log"

#Utilizei o módulo logging para registrar data, horário, ação e resultado em arquivo.
logging.basicConfig(
    filename=arquivoLog,
    level=logging.INFO,
    format="%(asctime)s | ação=%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def registrarLog(acao, resultado):
    logging.info("%s | resultado=%s", acao, resultado)
