import re
from flask import Flask, jsonify, request

app = Flask(__name__)

convidados = [
    {'id': 1, 'nome': 'Tiago', 'email': 'tiago@email.com'},
    {'id': 2, 'nome': 'Luiza', 'email': 'luiza@email.com'},
    {'id': 3, 'nome': 'Davi', 'email': 'davi@email.com'}
]

@app.route('/')
def bem_vindo():
    return 'Faculdade Impacta Tecnologia', 200

@app.route('/convidados', methods=['GET'])
def lista_convidados():
    return jsonify(convidados), 200

@app.route('/convidados/<int:id>', methods=['GET'])
def id_por_convidado(id):
    for convidado in convidados:
        if convidado['id'] == id:
            return jsonify(convidado), 200
    return jsonify({'mensagem': 'Convidado não encontrado'}), 404


@app.route('/convidados', methods=['POST'])
def adicionar_convidado():
    dados = request.get_json()

    nome = dados.get('nome', '')
    email = dados.get('email', '')

    def validar_email(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None

    if not nome or not email:
        return jsonify({'erro': 'Nome e e-mail são obrigatórios'}), 400

    if not validar_email(email):
        return jsonify({'erro': 'E-mail inválido'}), 400

    novo_id = len(convidados) + 1
    novo_convidado = {
        'id': novo_id,
        'nome': nome,
        'email': email
    }

    convidados.append(novo_convidado)
    return jsonify(novo_convidado), 201

@app.route('/convidados/<int:id>', methods=['PUT'])
def atualizar_convidado(id):
    dados = request.get_json()

    nome = dados.get('nome', '')
    email = dados.get('email', '')

    def validar_email(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None

    if not nome or not email:
        return jsonify({'erro': 'Nome e e-mail são obrigatórios'}), 400

    if not validar_email(email):
        return jsonify({'erro': 'E-mail inválido'}), 400

    for convidado in convidados:
        if convidado['id'] == id:
            convidado['nome'] = nome
            convidado['email'] = email
            return jsonify(convidado), 200

    return jsonify({'mensagem': 'Convidado não encontrado'}), 404

@app.route('/convidados/<int:id>', methods=['DELETE'])
def remover_convidado(id):
    for convidado in convidados:
        if convidado['id'] == id:
            convidados.remove(convidado)
            return jsonify({'mensagem': 'Convidado removido'})
    return jsonify({'mensagem': 'Convidado não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
