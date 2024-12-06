import api_test
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

products = [
    ("https://bersache.com/cdn/shop/files/13_8d3e7388-20cf-4e10-851f-1d285d11bffc.jpg?v=1693901022&width=1080", "sports shoes"),
    ("https://cdn.shopify.com/s/files/1/0767/4655/files/IG-FEED-0814_grande.JPG?v=1580934189", "banana yellow fruit"),
    ("https://5.imimg.com/data5/VN/YP/MY-33296037/orange-600x600-500x500.jpg", "orange fruit"),
    ("https://www.wildhorn.in/cdn/shop/products/915NPMLKRDL._SL1500.jpg?v=1703661630&width=1946", "brown wallet"),
    ("https://www.techtarget.com/rms/onlineimages/hp_elitebook_mobile.jpg", "grey laptop")
]

def display_image_pairs_with_similarity(image_urls, image_embeddings):
    """Display image pairs with their cosine similarities using Matplotlib."""
    num_images = len(image_urls)
    fig, axs = plt.subplots(num_images, num_images, figsize=(12, 12))
    
    # Adjust spacing between plots
    plt.subplots_adjust(wspace=0.5, hspace=0.5)  # Adjust horizontal and vertical spacing
    
    for i in range(num_images):
        for j in range(num_images):
            axs[i, j].axis("off")
            if True: #i != j
                similarity = cosine_similarity([image_embeddings[i]], [image_embeddings[j]])[0][0]
                img1 = api_test.fetch_image(image_urls[i])
                img2 = api_test.fetch_image(image_urls[j])
                
                combined_img = np.hstack((np.array(img1.resize((100, 100))), np.array(img2.resize((100, 100)))))
                axs[i, j].imshow(combined_img)
                axs[i, j].set_title(f"Sim: {similarity:.6f}", fontsize=8)
            """else:
                axs[i, j].text(0.5, 0.5, "Same Image", ha='center', va='center', fontsize=8, color='red')"""
    
    plt.show()

def main():
    image_embeddings = []
    text_embeddings = []
    image_urls = [product[0] for product in products]
    
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
        
    print("\nDisplaying image pairs with their similarities...")
    display_image_pairs_with_similarity(image_urls, image_embeddings)

    for i in image_embeddings:
        print(i)

main()