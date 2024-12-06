import streamlit as st
import requests
import psycopg2
from psycopg2.extras import execute_values
import os
import uuid

# Database connection setup
DB_HOST = "localhost"
DB_NAME = "ECommerceAI" 
DB_USER = "postgres"
DB_PASS = "" #Password
DB_PORT = 5433 #Port (Usually 5432)


# API Endpoints
IMAGE_EMBEDDINGS_API = "http://localhost:5000/get_image_embeddings"
TEXT_EMBEDDINGS_API = "http://localhost:5000/get_text_embeddings"

# Function to insert data into the database
def insert_product(data):
    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cursor = connection.cursor()

        # Insert into products table
        query = """
        INSERT INTO products (
            product_id, product_name, product_description, smart_search_phrase, 
            image_url, price, seller_name, seller_id, img_embeddings, txt_embeddings
        ) VALUES %s
        """
        execute_values(cursor, query, [data])
        connection.commit()
        st.success("Product successfully added to the database!")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Streamlit App
st.title("Admin Dashboard for E-Commerce")

# Product Form
st.header("Add New Product")
product_name = st.text_input("Product Name", placeholder="Enter product name")
product_description = st.text_area(
    "Product Description", placeholder="Enter product description"
)
smart_search_phrase = st.text_input(
    "Smart Search Phrase", placeholder="Enter search phrase (max 30 chars)"
)
price = st.number_input("Price", min_value=0.0, format="%.2f")
seller_name = st.text_input("Seller Name", placeholder="Enter seller name")
seller_id = st.text_input("Seller ID", placeholder="Enter seller ID")
image_file = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

if st.button("Submit"):
    if not (product_name and product_description and smart_search_phrase and price and seller_name and seller_id and image_file):
        st.error("All fields are required!")
    else:
        try:
            # Save the image locally
            image_id = str(uuid.uuid4())
            image_path = f"uploaded_images/{image_id}_{image_file.name}"
            os.makedirs("uploaded_images", exist_ok=True)
            with open(image_path, "wb") as f:
                f.write(image_file.read())

            # Get image embeddings
            with open(image_path, "rb") as img_file:
                img_response = requests.post(
                    IMAGE_EMBEDDINGS_API,
                    files={"image_file": img_file},
                )

            if img_response.status_code != 200:
                st.error(f"Image Embedding API Error: {img_response.json().get('error')}")
                st.stop()

            img_embeddings = img_response.json().get("image_embedding")

            # Get text embeddings
            text_response = requests.post(
                TEXT_EMBEDDINGS_API,
                json={"text": product_description},
            )

            if text_response.status_code != 200:
                st.error(f"Text Embedding API Error: {text_response.json().get('error')}")
                st.stop()

            txt_embeddings = text_response.json().get("text_embedding")

            # Prepare data for insertion
            product_id = str(uuid.uuid4())
            product_data = (
                product_id,
                product_name,
                product_description,
                smart_search_phrase,
                image_path,
                price,
                seller_name,
                seller_id,
                img_embeddings,
                txt_embeddings,
            )

            # Insert into database
            insert_product(product_data)

        except Exception as e:
            st.error(f"Error: {e}")
