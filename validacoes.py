from datetime import date, datetime
import re

TIPOS = ["Assédio verbal", "Assédio físico", "Importunação", "Outro"]
ESTADOS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
}


class ErroValidacao(Exception):
    pass


def validarTexto(valor, campo, minimo, maximo, obrigatorio=True):
    if valor is None:
        valor = ""
    if not isinstance(valor, str):
        raise ErroValidacao(f"O campo {campo} deve ser um texto.")
    valor = valor.strip()
    if obrigatorio and len(valor) < minimo:
        raise ErroValidacao(f"O campo {campo} é obrigatório.")
    if len(valor) > maximo:
        raise ErroValidacao(f"O campo {campo} excede o limite permitido.")
    return valor


def validarOcorrencia(dados):
    #Utilizei uma função única para aplicar as mesmas regras no POST e no PUT.
    if not isinstance(dados, dict):
        raise ErroValidacao("Envie os dados em formato JSON.")
    tipo = dados.get("tipo")
    if not isinstance(tipo, str) or tipo not in TIPOS:
        raise ErroValidacao("Selecione um tipo de ocorrência válido.")

    descricao = validarTexto(dados.get("descricao", ""), "descrição", 0, 500, False)
    local = validarTexto(dados.get("local"), "local", 3, 120)
    municipio = validarTexto(dados.get("municipio"), "município", 2, 100)
    estado = validarTexto(dados.get("estado"), "estado", 2, 2).upper()
    if estado not in ESTADOS:
        raise ErroValidacao("Informe uma sigla de estado brasileiro válida.")

    dataTexto = dados.get("dataOcorrencia")
    if not isinstance(dataTexto, str):
        raise ErroValidacao("Informe a data da ocorrência.")
    try:
        dataOcorrencia = datetime.strptime(dataTexto, "%Y-%m-%d").date()
    except ValueError:
        raise ErroValidacao("A data deve estar no formato AAAA-MM-DD.")
    if dataOcorrencia > date.today():
        raise ErroValidacao("A data da ocorrência não pode ser futura.")

    return {
        "tipo": tipo,
        "descricao": descricao,
        "local": local,
        "municipio": municipio,
        "estado": estado,
        "dataOcorrencia": dataOcorrencia
    }
