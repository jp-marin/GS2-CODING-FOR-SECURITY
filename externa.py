import requests

URL_ESTADOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"


def buscarEstados():
    #Utilizei requests para consumir a API pública do IBGE e tratar a resposta JSON.
    resposta = requests.get(URL_ESTADOS, timeout=8)
    resposta.raise_for_status()
    dados = resposta.json()
    if not isinstance(dados, list):
        raise ValueError("Formato inesperado recebido da API externa.")
    estados = [
        {"sigla": item["sigla"], "nome": item["nome"]}
        for item in dados
        if isinstance(item, dict) and "sigla" in item and "nome" in item
    ]
    return sorted(estados, key=lambda estado: estado["nome"])
