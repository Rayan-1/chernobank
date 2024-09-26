from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Dados simulados (em um sistema real, isso estaria em um banco de dados)
pix_keys = {}
users = {}
transactions = {}
user_limits = {}

# Limite diário e valores permitidos
DAILY_LIMIT = 1000.00
MINIMUM_VALUE = 0.01
MAXIMUM_VALUE = 9999999.99

def validar_chave_pix(chave: str) -> bool:
    """Valida a chave Pix"""
    # Valida CPF (11 dígitos)
    if re.fullmatch(r'\d{11}', chave):
        return True
    # Valida CNPJ (14 dígitos)
    if re.fullmatch(r'\d{14}', chave):
        return True
    # Valida Telefone (Formato: +5511999999999)
    if re.fullmatch(r'\+[1-9]{1}\d{1,14}', chave):
        return True
    # Valida E-mail
    if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', chave):
        return True
    
    return False

@app.route('/criar_chave_pix', methods=['POST'])
def criar_chave_pix():
    chave = request.json.get('chave')
    
    if chave in pix_keys:
        return jsonify({"message": "Chave Pix já existe! Tente cadastrar uma nova chave."}), 400

    if not validar_chave_pix(chave):
        return jsonify({"message": "Chave inválida! A chave deve ser um CPF, CNPJ, telefone ou e-mail válidos."}), 400

    pix_keys[chave] = {"valor": 0.0}
    transactions[chave] = []  
    return jsonify({"message": "Chave Pix criada com sucesso!"}), 201

@app.route('/validar_valor_pix', methods=['POST'])
def validar_valor_pix():
    valor = request.json.get('valor')
    if valor < MINIMUM_VALUE or valor > MAXIMUM_VALUE:
        return jsonify({"message": "Valor do Pix deve estar entre R$ 0.01 e R$ 9.999.999,99!"}), 400
    return jsonify({"message": "Valor do Pix validado com sucesso!"}), 200

@app.route('/realizar_pix', methods=['POST'])
def realizar_pix():
    chave = request.json.get('chave')
    valor = request.json.get('valor')

    if valor <= 0:
        return jsonify({"message": "Valor do Pix inválido!"}), 400

    # Verifica se a chave Pix existe
    if chave not in pix_keys:
        if valor <= 0:
            return jsonify({"message": "Chave e valor inválidos!"}), 400
        return jsonify({"message": "Chave Pix inválida!"}), 404

    try:
        valor = float(valor)  # Garantir que o valor seja um número de ponto flutuante
    except ValueError:
        return jsonify({"message": "Valor do Pix deve ser um número!"}), 400

    # Verifica o limite diário
    hoje = datetime.now().date()
    total_diario = 0.0

    for transacao in transactions[chave]:
        data_transacao = datetime.fromisoformat(transacao["data"]).date()
        if data_transacao == hoje:
            total_diario += float(transacao["valor"])  # Garantir que a comparação é feita com números

    # Verifica se o usuário tem um limite personalizado, caso contrário, usa o limite padrão
    limite_maximo = user_limits.get(chave, DAILY_LIMIT)

    if total_diario + valor > limite_maximo:
        excedente = (total_diario + valor) - limite_maximo
        return jsonify({
            "message": f"Limite diário excedido! Você tentou transferir R${valor:.2f}, mas o limite diário é R${limite_maximo:.2f}. Excesso: R${excedente:.2f}."
        }), 400

    # Simula a operação de Pix
    pix_keys[chave]["valor"] += valor
    formatted_value = f"{valor:.2f}"
    transactions[chave].append({"valor": formatted_value, "operacao": "entrada", "data": datetime.now().isoformat()})  # Registra a transação
    return jsonify({"message": "Pix realizado com sucesso!", "chave": chave, "valor": formatted_value}), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users and users[username] == password:
        return jsonify({"message": "Login bem-sucedido!"}), 200
    return jsonify({"message": "Usuário ou senha inválidos!"}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not (3 <= len(username) <= 15) or not re.match("^[a-zA-Z0-9]*$", username):
        return jsonify({"message": "Nome de usuário inválido! Deve ter entre 3 e 15 caracteres alfanuméricos."}), 400

    if not password.isdigit() or len(password) != 4:
        return jsonify({"message": "Senha inválida! Deve ser numérica e ter 4 dígitos."}), 400

    if username in users:
        return jsonify({"message": "Usuário já existe! Tente usar outra senha ou faça login."}), 400

    users[username] = password
    return jsonify({"message": "Cadastro bem-sucedido!"}), 201

@app.route('/extrato', methods=['POST'])
def extrato():
    chave = request.json.get('chave')
    if chave not in transactions:
        return jsonify({"message": "Chave Pix não encontrada!"}), 404
    
    return jsonify({"transacoes": transactions[chave]}), 200

@app.route('/definir_limite_diario', methods=['POST'])
def definir_limite_diario():
    chave = request.json.get('chave')
    novo_limite = request.json.get('novo_limite')

    if chave not in transactions:
        return jsonify({"message": "Chave Pix não encontrada!"}), 404

    try:
        novo_limite = float(novo_limite)
        if novo_limite <= 0:
            return jsonify({"message": "Limite diário inválido!"}), 400

        user_limits[chave] = novo_limite
        return jsonify({"message": f"Limite diário definido como R${novo_limite:.2f} com sucesso!"}), 200

    except ValueError:
        return jsonify({"message": "Limite deve ser um número!"}), 400

@app.route('/verificar_limite_diario', methods=['GET'])
def verificar_limite_diario():
    chave = request.args.get('chave')
    if chave not in transactions:
        return jsonify({"message": "Chave Pix não encontrada!"}), 404

    hoje = datetime.now().date()
    total_diario = sum(float(transacao["valor"]) for transacao in transactions[chave]
                       if datetime.fromisoformat(transacao["data"]).date() == hoje)

    limite_maximo = user_limits.get(chave, DAILY_LIMIT)
    excedido = total_diario > limite_maximo

    return jsonify({
        "total_diario": total_diario,
        "limite_maximo": limite_maximo,
        "excedido": excedido,
        "message": "Limite diário verificado com sucesso!"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
