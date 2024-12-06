from flask import Flask, request, jsonify
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
from io import BytesIO
import torch

app = Flask(__name__)

# Load CLIP Model and Processor
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

@app.route('/get_image_embeddings', methods=['POST'])
def get_image_embeddings():
    try:
        # Check if an image file is uploaded
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            image = Image.open(image_file)
        else:
            # Fallback to image URL
            data = request.json
            image_url = data.get('image_url')

            if not image_url:
                return jsonify({"error": "Either 'image_file' or 'image_url' is required."}), 400

            # Fetch the image from the URL
            response = requests.get(image_url)
            if response.status_code != 200:
                return jsonify({"error": "Failed to fetch image from the URL."}), 400

            image = Image.open(BytesIO(response.content))

        # Process image
        inputs = processor(images=image, return_tensors="pt", padding=True)

        # Generate image embeddings
        outputs = model.get_image_features(**inputs)
        image_embedding = outputs.squeeze(0).detach().cpu().numpy().tolist()  # Ensure dimensions are correct

        return jsonify({"image_embedding": image_embedding})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_text_embeddings', methods=['POST'])
def get_text_embeddings():
    try:
        data = request.json
        text = data.get('text')

        if not text:
            return jsonify({"error": "'text' is required."}), 400

        # Process text
        inputs = processor(text=[text], return_tensors="pt", padding=True)

        # Generate text embeddings
        outputs = model.get_text_features(**inputs)
        text_embedding = outputs.squeeze(0).detach().cpu().numpy().tolist()  # Ensure dimensions are correct

        return jsonify({"text_embedding": text_embedding})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
