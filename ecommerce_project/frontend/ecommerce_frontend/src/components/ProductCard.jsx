import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ShoppingCart, Plus } from 'lucide-react';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const ProductCard = ({ product }) => {
  const { addToCart, loading } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const result = await addToCart(product.id);
    if (result.success) {
      // Você pode adicionar uma notificação aqui
      console.log(result.message);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(price);
  };

  return (
    <Card className="group hover:shadow-lg transition-shadow duration-300">
      <CardHeader className="p-0">
        <div className="aspect-square overflow-hidden rounded-t-lg">
          <img
            src={product.image || '/placeholder-product.jpg'}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.src = '/placeholder-product.jpg';
            }}
          />
        </div>
      </CardHeader>
      
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">
          {product.name}
        </h3>
        
        {product.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {product.description}
          </p>
        )}
        
        <div className="flex items-center justify-between">
          <Badge variant="secondary" className="text-lg font-bold">
            {formatPrice(product.price)}
          </Badge>
        </div>
      </CardContent>
      
      <CardFooter className="p-4 pt-0">
        <Button 
          onClick={handleAddToCart}
          disabled={loading}
          className="w-full"
          size="sm"
        >
          <ShoppingCart className="h-4 w-4 mr-2" />
          {loading ? 'Adicionando...' : 'Adicionar ao Carrinho'}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;

