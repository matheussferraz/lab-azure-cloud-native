import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pyodbc
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

blobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobAccountName = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

# form do castro dos produtos
st.title('Cadastro de Produtos')
product_name = st.text_input("Nome do Produto")
product_description = st.text_area("Descrição do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = pyodbc.connect(DRIVER=SQL_SERVER, UID=SQL_USER, PWD=SQL_PASSWORD, DATABASE=SQL_DATABASE)
        cursor = conn.cursor()
        insert_query = """INSERT INTO Produto (nome, descricao, preco, imagem_url) VALUES (%s, %s, %s, %s)"""
        conn.execute(insert_query, (product_name, product_description, product_price, image_url))
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