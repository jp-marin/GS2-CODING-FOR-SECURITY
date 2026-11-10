# BEALIVE

## SOBRE O PROJETO

O BEalive é um projeto acadêmico desenvolvido com o objetivo de contribuir para a segurança das mulheres em espaços públicos. A plataforma permite registrar ocorrências de assédio e consultar os registros realizados.

O projeto está relacionado aos Objetivos de Desenvolvimento Sustentável (ODS) 5, 10 e 11, que abordam igualdade de gênero, redução das desigualdades e cidades e comunidades sustentáveis.

## TECNOLOGIAS UTILIZADAS

- Python e Flask para o desenvolvimento da API.
- MySQL para armazenar os registros.
- HTML, CSS e JavaScript para a interface.
- Requests para consultar a API do IBGE.
- Sockets TCP para comunicação entre cliente e servidor.

## FUNCIONALIDADES

- Cadastro de ocorrências.
- Consulta de ocorrências registradas.
- Edição e exclusão de registros.
- Consulta de estados brasileiros pela API do IBGE.
- Comunicação entre cliente e servidor por TCP.

## COMO EXECUTAR

1\. Instale as dependências com o comando:

```
pip install -r requirements.txt
```

2. Configure o banco de dados MySQL e execute o arquivo `schema.sql`.
3. Configure o arquivo `.env` com os dados de conexão do banco de dados e as configurações do servidor TCP.
4. Inicie a aplicação com o comando:

```
python app.py
```

5\. Acesse o endereço local informado no terminal pelo Flask.

## ESTRUTURA DO PROJETO

`app.py`: inicia a aplicação e define as rotas.

`banco.py`: realiza a conexão com o banco de dados.

`validacoes.py`: contém as validações dos dados.

`externa.py`: realiza consultas à API do IBGE.

`registros.py`: auxilia no gerenciamento das ocorrências.

`servidor.py` e `cliente.py`: realizam a comunicação TCP.

`schema.sql`: contém a estrutura do banco de dados.

`templates/`: armazena os arquivos HTML.

`static/`: armazena os arquivos CSS e JavaScript.

`logs/`: armazena os registros de execução.

## SEGURANÇA E LIMITAÇÕES

O projeto utiliza consultas SQL parametrizadas, validação de dados e arquivo `.env` para proteger as configurações de acesso.

Por ser um protótipo acadêmico, ainda não possui autenticação de usuários, moderação de ocorrências ou geolocalização automática. A plataforma também não substitui canais oficiais de denúncia ou serviços de emergência.

## OBJETIVO DO PROJETO

O BEalive busca demonstrar como a tecnologia pode contribuir para a organização de informações sobre situações de assédio e para a conscientização sobre a segurança das mulheres nos espaços públicos.