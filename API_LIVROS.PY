# API -  É UM LUGAR PARA DISPONIBILIZAR RECURSOS E / OU FUNCIONALIDADES
# 1. OBJETIVO - RIAR UM API DE DISPONIBILIZA A CONSULTA, CRIAÇÃO, EDIÇÃO E EXCLUSÃO DE LIVROS.
# 2. URL BASE - LOCALHOST.COM- YOUTUBE.COM/API/...
# 3. ENDPOINTS - FUNCIONALIDADES > 
#                 LOCALHOST/LIVROS (GET), LOCALHOST/LIVROS/ID()GET, LOCALHOST/LIVRO/ID(PUT), LOCALHOST/LIVRO/ID(DELETE)
# 4. QUAIS RECURSOS - LIVROS
from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {
        'id' : 1,
        'título': 'O Senhor dos Anéis - A Sociedade do Anel',
        'autor': 'J.R.R Tolkien'             
    },
    {
      'id' : 2,
        'título': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J.K Howling'
    },
        {
      'id' : 3,
        'título': 'James Clear',
        'autor': 'Hábitos Atômicos'
    },  
]
# CONSULTAR (TODOS)
@app.route('/livros',methods=['GET'])
def obter_livros():
    return jsonify(livros)


# CONSULTAR ID
@app.route('/livros/<int:id>',methods=['GET'])
def obter_livro_por_id(id):
    for livro in livros:
       if livro.get('id') == id:
            return jsonify(livro)
    
# EDITAR
@app.route('/livros/<int:id>',methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)    
            return jsonify(livros[indice])
    
# EXCLUIR    
app.run(port=5000, host='localhost', debug=True)