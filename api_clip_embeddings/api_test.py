import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time
from PIL import Image
from io import BytesIO

# API endpoints
IMAGE_API_URL = "http://127.0.0.1:5000/get_image_embeddings"
TEXT_API_URL = "http://127.0.0.1:5000/get_text_embeddings"

# Test data
products = [
    ("https://bersache.com/cdn/shop/files/13_8d3e7388-20cf-4e10-851f-1d285d11bffc.jpg?v=1693901022&width=1080", "sports shoes"),
    ("https://cdn.shopify.com/s/files/1/0767/4655/files/IG-FEED-0814_grande.JPG?v=1580934189", "banana yellow fruit"),
    ("https://5.imimg.com/data5/VN/YP/MY-33296037/orange-600x600-500x500.jpg", "orange fruit"),
    ("https://www.wildhorn.in/cdn/shop/products/915NPMLKRDL._SL1500.jpg?v=1703661630&width=1946", "brown wallet"),
    ("https://www.techtarget.com/rms/onlineimages/hp_elitebook_mobile.jpg", "grey laptop")
]

def get_image_embedding(image_url):
    """Fetch the image embedding from the Flask API and measure time taken."""
    start_time = time.time()
    response = requests.post(IMAGE_API_URL, json={"image_url": image_url})
    elapsed_time = time.time() - start_time
    if response.status_code == 200:
        print(f"Image embedding fetched in {elapsed_time:.2f} seconds.")
        return response.json().get("image_embedding")
    else:
        print(f"Error fetching image embedding: {response.status_code}, {response.text}")
        return None

def get_text_embedding(text):
    """Fetch the text embedding from the Flask API and measure time taken."""
    start_time = time.time()
    response = requests.post(TEXT_API_URL, json={"text": text})
    elapsed_time = time.time() - start_time
    if response.status_code == 200:
        print(f"Text embedding fetched in {elapsed_time:.2f} seconds.")
        return response.json().get("text_embedding")
    else:
        print(f"Error fetching text embedding: {response.status_code}, {response.text}")
        return None

def fetch_image(image_url):
    """Fetch the image from the URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Failed to fetch image: {response.status_code}")
        return None




def main():
    image_embeddings = []
    text_embeddings = []
    image_urls = [product[0] for product in products]
    
    # Fetch embeddings for all products
    for image_url, text in products:
        print(f"\nProcessing product: Image URL={image_url}, Text={text}")
        img_emb = get_image_embedding(image_url)
        txt_emb = get_text_embedding(text)
        
        if img_emb and txt_emb:
            image_embeddings.append(np.array(img_emb))
            text_embeddings.append(np.array(txt_emb))
        else:
            print("Failed to fetch embeddings for a product.")
            return
    
    # Calculate cosine similarities for image embeddings
    print("\nCosine Similarities between Image Embeddings:")
    for i in range(len(image_embeddings)):
        for j in range(i + 1, len(image_embeddings)):
            similarity = cosine_similarity([image_embeddings[i]], [image_embeddings[j]])
            print(f"Image {i} and Image {j}: {similarity[0][0]}")
    
    print("\nCosine Similarities between Text Embeddings:")
    for i in range(len(text_embeddings)):
        for j in range(i + 1, len(text_embeddings)):
            similarity = cosine_similarity([text_embeddings[i]], [text_embeddings[j]])
            print(f"Text {i} and Text {j}: {similarity[0][0]}")

    print(f"Embedding Size: {image_embeddings[0].shape}")

    """
    # Display image pairs with similarities
    print("\nDisplaying image pairs with their similarities...")
    display_image_pairs_with_similarity(image_urls, image_embeddings)

    for i in image_embeddings:
        print(i)"""

if __name__ == "__main__":
    main()
