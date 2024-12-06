const express = require("express");
const bodyParser = require("body-parser");
const { Pool } = require("pg");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
require("dotenv").config();
const path = require('path');


const app = express();
const port = process.env.PORT || 5000;


// Enable CORS for requests from the frontend
app.use(cors({ origin: "http://localhost:5173" }));


// PostgreSQL connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Middleware
app.use(bodyParser.json());

// Multer for image upload handling
const upload = multer({ storage: multer.memoryStorage() });

// Serve static images from the uploaded_images folder
app.use('/uploads', express.static(path.join(__dirname, '../admin_panel')));

// Get latest products
app.get("/api/products/latest", async (req, res) => {
  try {
    const result = await pool.query(
      "SELECT product_id, product_name, price, image_url FROM products ORDER BY product_id DESC LIMIT 10"
    );

    result.rows = result.rows.map(row => ({
      ...row,
      image_url: `http://localhost:${port}/uploads/${row.image_url}`
    }));

    res.json(result.rows);
  } catch (error) {
    console.error("Error fetching latest products:", error);
    res.status(500).json({ error: "Failed to fetch latest products" });
  }
});

// Search products by text
app.get("/api/products/search", async (req, res) => {
  const query = req.query.q;

  if (!query) {
    return res.status(400).json({ error: "Query parameter is required" });
  }

  try {
    const embeddingResponse = await axios.post(process.env.TEXT_EMBEDDING_API, {
      text: query,
    });

    //console.log("Embedding API Response:", embeddingResponse.data);

    const textEmbedding = embeddingResponse.data.text_embedding;
    const formattedEmbedding = JSON.stringify(textEmbedding);

    const result = await pool.query(
      `SELECT product_id, product_name, price, image_url, txt_embeddings <=> $1 AS similarity 
       FROM products 
       ORDER BY similarity 
       LIMIT 6`,
      [formattedEmbedding]
    );

    result.rows = result.rows.map(row => ({
      ...row,
      image_url: `http://localhost:${port}/uploads/${row.image_url}`
    }));

    /*// Log similarity scores to console
    // console.log(textEmbedding);
    result.rows.forEach((row) => {
      console.log(`Product ID: ${row.product_id}, Similarity: ${row.similarity}`);
    });*/

    res.json(result.rows);
  } catch (error) {
    console.error("Error during text search:", error);
    res.status(500).json({ error: "Failed to search products by text" });
  }
});

// Search products by image
const FormData = require('form-data');
const { Readable } = require('stream');

app.post("/api/products/similar", upload.single("image"), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "Image file is required" });
  }

  try {
    // Create a FormData instance
    const formData = new FormData();

    // Convert buffer to readable stream
    const bufferStream = new Readable();
    bufferStream.push(req.file.buffer);
    bufferStream.push(null);  // Signal the end of the stream

    // Append image file to formData
    formData.append("image_file", bufferStream, req.file.originalname);

    // Send the request with the form data
    const embeddingResponse = await axios.post(
      process.env.IMAGE_EMBEDDING_API,
      formData,
      { 
        headers: { 
          "Content-Type": "multipart/form-data", 
          ...formData.getHeaders() // Automatically add headers for multipart
        }
      }
    );

    const imageEmbedding = embeddingResponse.data.image_embedding;
    const formattedEmbedding = JSON.stringify(imageEmbedding);

    // Query your database using the embedding
    const result = await pool.query(
      `SELECT product_id, product_name, price, image_url, img_embeddings <=> $1 AS similarity
       FROM products 
       ORDER BY img_embeddings <=> $1 
       LIMIT 6`,
      [formattedEmbedding]
    );

    result.rows = result.rows.map(row => ({
      ...row,
      image_url: `http://localhost:${port}/uploads/${row.image_url}`
    }));

    res.json(result.rows);
  } catch (error) {
    console.error("Error during image search:", error);
    res.status(500).json({ error: "Failed to search products by image" });
  }
});


// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
