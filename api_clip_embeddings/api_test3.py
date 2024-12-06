import api_test
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

products = [
    ("https://bersache.com/cdn/shop/files/13_8d3e7388-20cf-4e10-851f-1d285d11bffc.jpg?v=1693901022&width=1080", "sports shoes"),
    ("https://cdn.shopify.com/s/files/1/0767/4655/files/IG-FEED-0814_grande.JPG?v=1580934189", "banana yellow fruit"),
    ("https://5.imimg.com/data5/VN/YP/MY-33296037/orange-600x600-500x500.jpg", "orange fruit"),
    ("https://www.wildhorn.in/cdn/shop/products/915NPMLKRDL._SL1500.jpg?v=1703661630&width=1946", "brown wallet"),
    ("https://www.techtarget.com/rms/onlineimages/hp_elitebook_mobile.jpg", "grey laptop")
]

def plot_embeddings_pca(embeddings, labels, title):
    """
    Visualize 512-dimensional embeddings in 2D space using PCA.
    
    :param embeddings: List of embeddings (each of size 512).
    :param labels: List of labels (text or indices corresponding to images).
    :param title: Title for the plot.
    :param is_image: Boolean indicating whether labels correspond to images.
    :param image_urls: URLs for images (if is_image is True).
    """
    # Perform PCA to reduce to 2D
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)
    
    plt.figure(figsize=(12, 8))
    
    for i, (x, y) in enumerate(reduced_embeddings):
        # Plot the text label
        plt.scatter(x, y, label=f"{labels[i]}")
        plt.text(x + 0.01, y + 0.01, labels[i], fontsize=9)
    
    plt.title(title)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    image_embeddings = []
    text_embeddings = []
    image_urls = [product[0] for product in products]
    texts = [product[1] for product in products]
    
    # Fetch embeddings for all products
    for image_url, text in products:
        print(f"\nProcessing product: Image URL={image_url}, Text={text}")
        img_emb = api_test.get_image_embedding(image_url)
        txt_emb = api_test.get_text_embedding(text)
        
        if img_emb and txt_emb:
            image_embeddings.append(np.array(img_emb))
            text_embeddings.append(np.array(txt_emb))
        else:
            print("Failed to fetch embeddings for a product.")
            return
        

    # Visualize embeddings in 2D using PCA
    plot_embeddings_pca(text_embeddings, texts, title="Text Embeddings in 2D")

main()