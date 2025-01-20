from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

#carrega variaveis de ambiente
load_dotenv()

#url do banco
MONGO_URL = os.getenv('MONGO_URL')


#criar e retornar conexão
def get_mongo_client():
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000) #timeout de 5 segundos
        #testando a conexão
        client.admin.command('ping')                                 #ping no servidor
        print("COnexão com mongoDB estabelecida com sucesso.")
        return client
    except errors.ServerSelectionTimeoutError as err:
        print(f'Erro ao conectar ao MongoDB: {err}')