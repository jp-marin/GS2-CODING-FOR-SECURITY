# BEalive — Relatório Global Solution
**Disciplina:** Coding for Security  
**Integrante:** [SEU NOME]  
**Turma:** [SUA TURMA]

## 1. Problema, cidadão e ODS
O BEalive aborda a dificuldade de encontrar informações colaborativas sobre relatos de assédio em espaços públicos, como ruas e transportes. O público afetado considerado é formado por mulheres que circulam nesses espaços e pela comunidade que pode utilizar informações agregadas para conscientização.

**Evidência real do problema:** [INSIRA UMA EVIDÊNCIA QUE VOCÊ REALMENTE COLETOU: conversa autorizada, observação documentada ou dado público. Informe fonte, data e contexto. Não invente depoimentos ou números.]

A solução se relaciona diretamente ao ODS 11 — Cidades e Comunidades Sustentáveis, pois trata da segurança e do uso dos espaços urbanos. Para respeitar a lista de ODS apresentada no enunciado da disciplina, o relatório considera também o ODS 10 — Redução das Desigualdades. O tema possui relação conceitual com o ODS 5, embora ele não esteja na lista de ODS apresentada no PDF da atividade.

## 2. Arquitetura e modelo de dados
A aplicação utiliza Flask para disponibilizar uma API REST e servir a interface HTML. O JavaScript consome os endpoints da própria aplicação. O MySQL armazena os relatos, acessado diretamente por Python com `mysql-connector-python`, sem ORM. A API pública do IBGE é consultada por `requests`, com resposta JSON, para carregar estados brasileiros. Um módulo TCP separado demonstra comunicação cliente-servidor por sockets.

A tabela `ocorrencias` possui: `id` (chave primária), `tipo`, `descricao` (opcional), `local`, `municipio`, `estado`, `data_ocorrencia` e `criado_em`. O sistema permite criar, consultar, atualizar e excluir registros.

## 3. Segurança, validação e ameaças
As credenciais são mantidas em `.env`; o `.env.example` contém apenas valores ilustrativos. As consultas SQL são parametrizadas. O servidor valida tipo, tamanho, campos obrigatórios, sigla de estado e formato/data da ocorrência. As respostas de erro não expõem detalhes internos. A coleta é mínima: não são solicitados nome, telefone, CPF ou e-mail. A demonstração deve utilizar dados fictícios ou abertos.

Ameaças consideradas:
1. **SQL injection:** mitigada por parâmetros SQL e validação de entradas.
2. **Exposição de dados pessoais em relatos:** mitigada por não solicitar identificadores, limitar a descrição e orientar que não sejam inseridos dados identificáveis.
3. **Indisponibilidade/abuso de requisições ou falha externa:** mitigada parcialmente por validação, timeout, tratamento de exceções e mensagens genéricas. O protótipo não implementa autenticação nem limitação de taxa.

**Validação realizada:** [PREENCHA COM OS TESTES QUE VOCÊ EXECUTOU, os códigos HTTP observados e eventuais correções. Não declare testes que não realizou.]

## 4. Limitações e viabilidade
O protótipo não verifica a veracidade dos relatos e a quantidade de registros não comprova o nível real de risco de uma região. Não possui autenticação, moderação, geolocalização ou integração com serviços de emergência. A consulta ao IBGE depende de internet. A solução demonstra viabilidade técnica como ferramenta acadêmica de conscientização, mas não deve ser utilizada isoladamente para decisões de segurança.

## 5. Declaração de uso de inteligência artificial
[ADAPTE COM TRANSPARÊNCIA À SUA UTILIZAÇÃO REAL. Exemplo: “Utilizei inteligência artificial como apoio para compreender o enunciado, estruturar o desenvolvimento, revisar trechos de código e elaborar casos de teste. Revisei, executei e estudei os componentes entregues, sendo responsável pela validação e pela explicação do funcionamento do projeto.” Descreva a ferramenta utilizada e as atividades reais. Não declare que revisou ou executou algo que não fez.]
