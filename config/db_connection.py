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
        print("Conexão com mongoDB estabelecida com sucesso.")
        return client
    except errors.ServerSelectionTimeoutError as err:
        print(f'Erro ao conectar ao MongoDB: {err}')


# para executar a função:
if __name__ == "__main__":
    try:
        client = get_mongo_client()
        print("Teste concluido: Conexão com MongoDB bem-sucedida!")
    except Exception as e:
        print(f"Erro no teste de conexão com MongoDB: {e}")


"""
Utilizar a conexão em outro pagina:

from config.db_connection import get_mongo_client

client = get_mongo_client()
db = client['empresa_ficticia']
clientes_collection = db['clientes']

restante do codigo.........

"""