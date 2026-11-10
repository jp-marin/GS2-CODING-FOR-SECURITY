from flask import Flask, jsonify, request, render_template
from mysql.connector import Error as ErroMySQL
from banco import conectar
from validacoes import validarOcorrencia, ErroValidacao
from externa import buscarEstados
from registros import registrarLog

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.get("/api/estados")
def estados():
    try:
        dados = buscarEstados()
        registrarLog("CONSULTA_ESTADOS", "SUCESSO")
        return jsonify(dados), 200
    except Exception:
        registrarLog("CONSULTA_ESTADOS", "ERRO")
        return jsonify({"erro": "Não foi possível consultar os estados agora."}), 502


@app.get("/api/ocorrencias")
def listarOcorrencias():
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        #Utilizei ORDER BY para apresentar primeiro os relatos mais recentes
        cursor.execute("""
            SELECT id, tipo, descricao, local, municipio, estado,
                   DATE_FORMAT(data_ocorrencia, '%Y-%m-%d') AS dataOcorrencia
            FROM ocorrencias
            ORDER BY data_ocorrencia DESC, id DESC
        """)
        dados = cursor.fetchall()
        registrarLog("LISTAR_OCORRENCIAS", "SUCESSO")
        return jsonify(dados), 200
    except ErroMySQL:
        registrarLog("LISTAR_OCORRENCIAS", "ERRO_BANCO")
        return jsonify({"erro": "Não foi possível consultar os registros."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


@app.get("/api/ocorrencias/<int:id>")
def consultarOcorrencia(id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        #Utilizei parâmetro %s para impedir que o valor recebido seja executado como SQL
        cursor.execute("""
            SELECT id, tipo, descricao, local, municipio, estado,
                   DATE_FORMAT(data_ocorrencia, '%Y-%m-%d') AS dataOcorrencia
            FROM ocorrencias WHERE id = %s
        """, (id,))
        dado = cursor.fetchone()
        if not dado:
            registrarLog("CONSULTAR_OCORRENCIA", "NAO_ENCONTRADO")
            return jsonify({"erro": "Registro não encontrado."}), 404
        registrarLog("CONSULTAR_OCORRENCIA", "SUCESSO")
        return jsonify(dado), 200
    except ErroMySQL:
        registrarLog("CONSULTAR_OCORRENCIA", "ERRO_BANCO")
        return jsonify({"erro": "Não foi possível consultar o registro."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


@app.post("/api/ocorrencias")
def criarOcorrencia():
    conexao = None
    cursor = None
    try:
        dados = validarOcorrencia(request.get_json(silent=True))
        conexao = conectar()
        cursor = conexao.cursor()
        #Utilizei parâmetros em todos os campos recebidos para evitar SQL injection
        cursor.execute("""
            INSERT INTO ocorrencias
            (tipo, descricao, local, municipio, estado, data_ocorrencia)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            dados["tipo"], dados["descricao"], dados["local"],
            dados["municipio"], dados["estado"], dados["dataOcorrencia"]
        ))
        conexao.commit()
        novoId = cursor.lastrowid
        registrarLog("CRIAR_OCORRENCIA", "SUCESSO")
        return jsonify({"mensagem": "Relato registrado.", "id": novoId}), 201
    except ErroValidacao as erro:
        registrarLog("CRIAR_OCORRENCIA", "DADOS_INVALIDOS")
        return jsonify({"erro": str(erro)}), 400
    except ErroMySQL:
        if conexao:
            conexao.rollback()
        registrarLog("CRIAR_OCORRENCIA", "ERRO_BANCO")
        return jsonify({"erro": "Não foi possível registrar o relato."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


@app.put("/api/ocorrencias/<int:id>")
def atualizarOcorrencia(id):
    conexao = None
    cursor = None
    try:
        dados = validarOcorrencia(request.get_json(silent=True))
        conexao = conectar()
        cursor = conexao.cursor()
        #Utilizei uma consulta prévia para diferenciar registro inexistente de dados sem alteração
        cursor.execute("SELECT id FROM ocorrencias WHERE id = %s", (id,))
        if cursor.fetchone() is None:
            registrarLog("ATUALIZAR_OCORRENCIA", "NAO_ENCONTRADO")
            return jsonify({"erro": "Registro não encontrado."}), 404
        cursor.execute("""
            UPDATE ocorrencias
            SET tipo = %s, descricao = %s, local = %s, municipio = %s,
                estado = %s, data_ocorrencia = %s
            WHERE id = %s
        """, (
            dados["tipo"], dados["descricao"], dados["local"],
            dados["municipio"], dados["estado"], dados["dataOcorrencia"], id
        ))
        conexao.commit()
        registrarLog("ATUALIZAR_OCORRENCIA", "SUCESSO")
        return jsonify({"mensagem": "Relato atualizado."}), 200
    except ErroValidacao as erro:
        registrarLog("ATUALIZAR_OCORRENCIA", "DADOS_INVALIDOS")
        return jsonify({"erro": str(erro)}), 400
    except ErroMySQL:
        if conexao:
            conexao.rollback()
        registrarLog("ATUALIZAR_OCORRENCIA", "ERRO_BANCO")
        return jsonify({"erro": "Não foi possível atualizar o relato."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


@app.delete("/api/ocorrencias/<int:id>")
def excluirOcorrencia(id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM ocorrencias WHERE id = %s", (id,))
        if cursor.rowcount == 0:
            registrarLog("EXCLUIR_OCORRENCIA", "NAO_ENCONTRADO")
            return jsonify({"erro": "Registro não encontrado."}), 404
        conexao.commit()
        registrarLog("EXCLUIR_OCORRENCIA", "SUCESSO")
        return jsonify({"mensagem": "Relato excluído."}), 200
    except ErroMySQL:
        if conexao:
            conexao.rollback()
        registrarLog("EXCLUIR_OCORRENCIA", "ERRO_BANCO")
        return jsonify({"erro": "Não foi possível excluir o relato."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


@app.errorhandler(404)
def rotaNaoEncontrada(erro):
    return jsonify({"erro": "Recurso não encontrado."}), 404


@app.errorhandler(405)
def metodoNaoPermitido(erro):
    return jsonify({"erro": "Método não permitido."}), 405


if __name__ == "__main__":
    #Utilizei o modo debug desligado para não expor informações internas ao usuário
    app.run(host="127.0.0.1", port=5000, debug=False)
