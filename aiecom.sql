CREATE EXTENSION vector;

CREATE TABLE products (
  product_id TEXT PRIMARY KEY,
  product_name TEXT NOT NULL,
  product_description TEXT NOT NULL, 
  smart_search_phrase VARCHAR(30) NOT NULL,
  image_url TEXT NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  seller_name TEXT NOT NULL,
  seller_id TEXT NOT NULL,
  img_embeddings VECTOR(512),
  txt_embeddings VECTOR(512)
);