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

SQL_DRIVER = os.getenv('SQL_DRIVER')
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

# form do castro dos produtos MM
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

        conn = pyodbc.connect(
            f"DRIVER={SQL_DRIVER};"
            f"SERVER={SQL_SERVER};" 
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USER};"
            f"PWD={SQL_PASSWORD}"
        )
        cursor = conn.cursor()
        insert_query = """INSERT INTO Produtos (nome, descricao, preco, imagem_url) VALUES (?, ?, ?, ?)"""

        cursor.execute(insert_query, (product_name, product_description, product_price, image_url))
        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        st.error(f'Erro ao inserir produto: {e}')
        return False

def list_products_sql():
    try:
        conn = pyodbc.connect(
            f"DRIVER={SQL_DRIVER};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USER};"
            f"PWD={SQL_PASSWORD}"
        )
        cursor = conn.cursor()
        select_query = "SELECT id, nome, descricao, preco, imagem_url FROM Produtos"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

def list_products_screen():
    products = list_products_sql()
    if products:
        for product in products:
            st.image(product.imagem_url, width=100)
            st.write(f"**Nome:** {product.nome}")
            st.write(f"**Descrição:** {product.descricao}")
            st.write(f"**Preço:** R$ {product.preco:.2f}")
            st.write("---")
    else:
        st.write("Nenhum produto encontrado.")

if st.button("Salvar Produto"):
    insert_product(product_name, product_price, product_description, product_image)
    products = list_products_screen()
    return_message = 'Produto Salvo com sucesso'

st.header("Produtos Cadastrados")

if st.button("Listar Produto"):
    try:
        products = list_products_screen()
        if products:
            st.success('Produtos listados com sucesso')
    except Exception as e:
        st.error(f'Erro ao listar produtos: {e}')
