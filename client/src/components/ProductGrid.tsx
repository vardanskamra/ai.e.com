import React from 'react';
import ProductCard from './ProductCard';

interface Product {
  product_id: number;
  product_name: string;
  price: number;
  image_url: string;
  similarity?: number;
}

interface ProductGridProps {
  products: Product[];
  loading: boolean;
  onLoadMore: () => void;
  hasMore: boolean;
}

export default function ProductGrid({ products, loading, onLoadMore, hasMore }: ProductGridProps) {
  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <ProductCard key={product.product_id} product={product} />
        ))}
      </div>
      
      {loading && (
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}
      
      {!loading && hasMore && (
        <div className="flex justify-center">
          <button
            onClick={onLoadMore}
            className="px-6 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Load More
          </button>
        </div>
      )}
    </div>
  );
}