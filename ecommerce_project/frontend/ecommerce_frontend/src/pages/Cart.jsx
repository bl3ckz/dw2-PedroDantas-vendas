import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { ShoppingCart, Plus, Minus, Trash2, ArrowLeft, CreditCard } from 'lucide-react';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';

const Cart = () => {
  const { cart, loading, updateCartItem, removeFromCart, checkout } = useCart();
  const { isAuthenticated } = useAuth();
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(price);
  };

  const handleUpdateQuantity = async (productId, newQuantity) => {
    if (newQuantity < 1) return;
    await updateCartItem(productId, newQuantity);
  };

  const handleRemoveItem = async (productId) => {
    await removeFromCart(productId);
    setMessage({ type: 'success', text: 'Item removido do carrinho' });
    setTimeout(() => setMessage({ type: '', text: '' }), 3000);
  };

  const handleCheckout = async () => {
    setCheckoutLoading(true);
    const result = await checkout();
    
    if (result.success) {
      setMessage({ type: 'success', text: 'Pedido finalizado com sucesso!' });
      setTimeout(() => {
        setMessage({ type: '', text: '' });
        navigate('/');
      }, 2000);
    } else {
      setMessage({ type: 'error', text: result.message });
    }
    
    setCheckoutLoading(false);
  };

  const calculateTotal = () => {
    return cart.items?.reduce((total, item) => {
      return total + (item.product?.price || 0) * item.quantity;
    }, 0) || 0;
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center mb-8">
        <Link to="/products">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Continuar Comprando
          </Button>
        </Link>
      </div>

      <h1 className="text-3xl font-bold mb-8">Carrinho de Compras</h1>

      {message.text && (
        <Alert className={`mb-6 ${message.type === 'error' ? 'border-red-500' : 'border-green-500'}`}>
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      )}

      {loading ? (
        <div className="text-center py-8">
          <p>Carregando carrinho...</p>
        </div>
      ) : !cart.items || cart.items.length === 0 ? (
        <div className="text-center py-16">
          <ShoppingCart className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Seu carrinho está vazio</h3>
          <p className="text-gray-600 mb-6">
            Adicione alguns produtos incríveis ao seu carrinho
          </p>
          <Link to="/products">
            <Button>
              Ver Produtos
            </Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Items do Carrinho */}
          <div className="lg:col-span-2 space-y-4">
            {cart.items.map((item) => (
              <Card key={`${item.order_id}-${item.product_id}`}>
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    {/* Imagem do Produto */}
                    <div className="w-20 h-20 flex-shrink-0">
                      <img
                        src={item.product?.image || '/placeholder-product.jpg'}
                        alt={item.product?.name}
                        className="w-full h-full object-cover rounded-lg"
                        onError={(e) => {
                          e.target.src = '/placeholder-product.jpg';
                        }}
                      />
                    </div>

                    {/* Informações do Produto */}
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">
                        {item.product?.name}
                      </h3>
                      <p className="text-gray-600 text-sm">
                        {item.product?.description}
                      </p>
                      <Badge variant="secondary" className="mt-2">
                        {formatPrice(item.product?.price || 0)}
                      </Badge>
                    </div>

                    {/* Controles de Quantidade */}
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleUpdateQuantity(item.product_id, item.quantity - 1)}
                        disabled={item.quantity <= 1 || loading}
                      >
                        <Minus className="h-4 w-4" />
                      </Button>
                      
                      <span className="w-12 text-center font-semibold">
                        {item.quantity}
                      </span>
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}
                        disabled={loading}
                      >
                        <Plus className="h-4 w-4" />
                      </Button>
                    </div>

                    {/* Botão Remover */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveItem(item.product_id)}
                      disabled={loading}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Resumo do Pedido */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle>Resumo do Pedido</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between">
                  <span>Subtotal:</span>
                  <span>{formatPrice(calculateTotal())}</span>
                </div>
                
                <div className="flex justify-between">
                  <span>Frete:</span>
                  <span className="text-green-600">Grátis</span>
                </div>
                
                <hr />
                
                <div className="flex justify-between text-lg font-semibold">
                  <span>Total:</span>
                  <span>{formatPrice(calculateTotal())}</span>
                </div>

                <Button
                  onClick={handleCheckout}
                  disabled={checkoutLoading || loading}
                  className="w-full"
                  size="lg"
                >
                  <CreditCard className="h-4 w-4 mr-2" />
                  {checkoutLoading ? 'Finalizando...' : 'Finalizar Pedido'}
                </Button>

                <p className="text-sm text-gray-600 text-center">
                  Simulação de checkout para fins educacionais
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart;

