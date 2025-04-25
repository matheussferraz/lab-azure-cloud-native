import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import pyodbc
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

def upload_image(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)

        blob_client.upload_blob(file.read(), overwrite=True)

        product_image = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
        return None





blob_service_client = BlobServiceClient.from_connection_string(os.getenv("BLOB_CONNECTION_STRING"))
container_client = blob_service_client.get_container_client(os.getenv('BLOB_CONTAINER_NAME'))
blob_client = container_client.get_blob_client(os.getenv('BLOB_ACCOUNT_NAME'))

def upload_blob(connection_string, container_name, blob_name, data):
    try:
        # Cria o BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Obtém o ContainerClient
        container_client = blob_service_client.get_container_client(container_name)
        
        # Cria o BlobClient
        blob_client = container_client.get_blob_client(blob_name)
        
        # Faz upload do blob
        blob_client.upload_blob(data)
        
        print(f"Upload do blob {blob_name} concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao fazer upload do blob: {e}")
        raise
        
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

st.title('Cadastro de Produtos')

product_name = st.text_input("Nome do Produto")
product_description = st.text_area("Descrição do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

def upload_image(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)

        blob_client.upload_blob(file.read(), overwrite=True)

        product_image = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
        return None

def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = pyodbc.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor.conn.cursor()
        cursor.execute(insert_query, (product_data["nome"], product_data["descricao"], product_price["preco"], product_data["imagem_url"]))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao inserir produto: {e}')
        return False

if st.button("Salvar Produto"):
    insert_product(product_name, product_price, product_description, product_image)
    return_message = 'Produto Salvo com sucesso'

st.header("Produtos Cadastrados")

if st.button("Listar Produto"):
    return_message = 'Produtos listados com sucesso'