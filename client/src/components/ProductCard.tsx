import React from 'react';

interface Product {
  product_id: number;
  product_name: string;
  price: number;
  image_url: string;
  similarity?: number;
}

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="aspect-square overflow-hidden">
        <img
          src={product.image_url}
          alt={product.product_name}
          className="w-full h-full object-cover hover:scale-105 transition-transform"
        />
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{product.product_name}</h3>
        <div className="flex justify-between items-center">
          <span className="text-xl font-bold">₹{product.price}</span>
          {product.similarity !== undefined && (
            <span className="text-sm text-gray-500">
              Similarity: {(1 - product.similarity).toFixed(3)}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}