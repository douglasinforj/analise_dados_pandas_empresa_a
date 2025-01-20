from pymongo import MongoClient, ASCENDING
from faker import Faker
import random
from datetime import datetime, timedelta

import sys
import os

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Importar o módulo de conexão
from config.db_connection import get_mongo_client

# Configurando acesso ao banco
fake = Faker('pt_BR')
client = get_mongo_client()
db = client['empresa_a']



# Função para garantir que as coleções existam
def criar_colecoes_se_nao_existirem():
    # Garantir que as coleções sejam criadas
    if "clientes" not in db.list_collection_names():
        db.create_collection("clientes")
    if "produtos" not in db.list_collection_names():
        db.create_collection("produtos")
    if "pedidos" not in db.list_collection_names():
        db.create_collection("pedidos")



# Configurando esquema de validação
def configurar_esquema():
    criar_colecoes_se_nao_existirem()

    # Configura Esquema de Validação para clientes
    db.command({
        "collMod": "clientes",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["nome", "cpf", "idade", "endereco"],
                "properties": {
                    "nome": {"bsonType": "string", "description": "Nome do cliente"},
                    "cpf": {"bsonType": "string", "pattern": r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", "description": "CPF válido"},
                    "idade": {"bsonType": "int", "minimum": 18, "maximum": 100, "description": "Idade entre 18 e 100"},
                    "endereco": {
                        "bsonType": "object",
                        "required": ["rua", "numero", "bairro", "cidade", "estado", "cep"],
                        "properties": {
                            "rua": {"bsonType": "string"},
                            "numero": {"bsonType": "string"},
                            "bairro": {"bsonType": "string"},
                            "cidade": {"bsonType": "string"},
                            "estado": {"bsonType": "string"},
                            "cep": {"bsonType": "string"}
                        }
                    }
                }
            }
        }
    })

    # Esquema de validação para produtos
    db.command({
        "collMod": "produtos",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["nome", "categoria", "preco", "custo"],
                "properties": {
                    "nome": {"bsonType": "string"},
                    "categoria": {"bsonType": "string"},
                    "preco": {"bsonType": "double", "minimum": 0},
                    "custo": {"bsonType": "double", "minimum": 0}
                }
            }
        }
    })

    # Esquema de validação para pedidos
    db.command({
        "collMod": "pedidos",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["cliente_id", "nome_cliente", "data_pedido", "itens", "total_pedido"],
                "properties": {
                    "cliente_id": {"bsonType": "objectId"},
                    "nome_cliente": {"bsonType": "string"},
                    "data_pedido": {"bsonType": "date"},
                    "itens": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["produto_id", "nome_produto", "quantidade", "preco_unitario", "total_item"],
                            "properties": {
                                "produto_id": {"bsonType": "objectId"},
                                "nome_produto": {"bsonType": "string"},
                                "quantidade": {"bsonType": "int", "minimum": 1},
                                "preco_unitario": {"bsonType": "double", "minimum": 0},
                                "total_item": {"bsonType": "double", "minimum": 0}
                            }
                        }
                    },
                    "total_pedido": {"bsonType": "double", "minimum": 0}
                }
            }
        }
    })

# Executar funções
if __name__ == "__main__":
    print("Configurando coleções e validações")
    configurar_esquema()
    print("Esquema configurado.")
