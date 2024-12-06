import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import ProductGrid from './components/ProductGrid';
import { ShoppingBag } from 'lucide-react';

interface Product {
  product_id: number;
  product_name: string;
  price: number;
  image_url: string;
  similarity?: number;
}

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [visibleProducts, setVisibleProducts] = useState(6);

  useEffect(() => {
    fetchLatestProducts();
  }, []);

  const fetchLatestProducts = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:3000/api/products/latest');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching latest products:', error);
    }
    setLoading(false);
  };

  const handleSearch = async (query: string) => {
    setLoading(true);
    setVisibleProducts(6);
    try {
      const response = await fetch(`http://localhost:3000/api/products/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error searching products:', error);
    }
    setLoading(false);
  };

  const handleImageUpload = async (file: File) => {
    setLoading(true);
    setVisibleProducts(6);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:3000/api/products/similar', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error searching by image:', error);
    }
    setLoading(false);
  };

  const handleLoadMore = () => {
    setVisibleProducts((prev) => Math.min(prev + 6, products.length));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center gap-2">
            <ShoppingBag className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Smart Shop</h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 pb-12">
        <SearchBar onSearch={handleSearch} onImageUpload={handleImageUpload} />
        <ProductGrid
          products={products.slice(0, visibleProducts)}
          loading={loading}
          onLoadMore={handleLoadMore}
          hasMore={visibleProducts < products.length}
        />
      </main>
    </div>
  );
}

export default App;