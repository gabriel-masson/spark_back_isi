from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
#Conexão com o MongoDB
client = MongoClient("mongodb+srv://mongoISI321:mongoISI321@cluster0.6gl4cs4.mongodb.net/?retryWrites=true&w=majority")
db = client['mydb']
collection = db['alunosISI']


@app.route('/api/aluno', methods=['GET'])
def get_alunos():
    docs = [doc for doc in collection.find()]
    
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    return jsonify(docs)


@app.route('/api/aluno', methods=['POST'])
def post_aluno():
    dados = request.get_json()
    
    #inserção de dados
    result = collection.insert_one({
        'uuid': uuid.uuid4().hex,
        'nome': dados['nome'],
        'idade': dados['idade'],
        'titulo': dados['titulo'],
        'linha_de_pesquisa': dados['linha_de_pesquisa']
    })
    
    return str(result.inserted_id)


@app.route('/api/aluno', methods=['PUT'])
def put_aluno():
    dados = request.get_json()
    result = collection.update_one({'uuid': dados['id']}, {
        '$set': {
            'nome': dados['nome'],
            'idade': dados['idade'],
            'titulo': dados['titulo'],
            'linha_de_pesquisa': dados['linha_de_pesquisa']
        }
    })
    return str(result.modified_count)


@app.route('/api/aluno/<id>', methods=['DELETE'])
def delete_aluno(id):
    result = collection.delete_one({'uuid': id})
    return str(result.deleted_count)

if __name__ == '__main__':
    app.run(debug=True)
