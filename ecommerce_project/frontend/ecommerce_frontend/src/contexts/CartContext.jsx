import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart deve ser usado dentro de um CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState({ items: [], total: 0 });
  const [loading, setLoading] = useState(false);
  const { token, isAuthenticated } = useAuth();

  // Carregar carrinho quando usuário fizer login
  useEffect(() => {
    if (isAuthenticated) {
      fetchCart();
    } else {
      setCart({ items: [], total: 0 });
    }
  }, [isAuthenticated]);

  const fetchCart = async () => {
    if (!token) return;
    
    try {
      const response = await fetch('/api/cart', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setCart(data.cart);
      }
    } catch (error) {
      console.error('Erro ao carregar carrinho:', error);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    if (!token) return { success: false, message: 'Faça login para adicionar ao carrinho' };
    
    setLoading(true);
    try {
      const response = await fetch('/api/cart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ product_id: productId, quantity }),
      });

      const data = await response.json();

      if (response.ok) {
        setCart(data.cart);
        return { success: true, message: 'Produto adicionado ao carrinho' };
      } else {
        return { success: false, message: data.message };
      }
    } catch (error) {
      return { success: false, message: 'Erro de conexão' };
    } finally {
      setLoading(false);
    }
  };

  const updateCartItem = async (productId, quantity) => {
    if (!token) return;
    
    setLoading(true);
    try {
      const response = await fetch(`/api/cart/item/${productId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ quantity }),
      });

      if (response.ok) {
        const data = await response.json();
        setCart(data.cart);
      }
    } catch (error) {
      console.error('Erro ao atualizar item:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = async (productId) => {
    if (!token) return;
    
    setLoading(true);
    try {
      const response = await fetch(`/api/cart/item/${productId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setCart(data.cart);
      }
    } catch (error) {
      console.error('Erro ao remover item:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkout = async () => {
    if (!token) return { success: false, message: 'Faça login para finalizar pedido' };
    
    setLoading(true);
    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setCart({ items: [], total: 0 });
        return { success: true, message: 'Pedido finalizado com sucesso', order: data.order };
      } else {
        return { success: false, message: data.message };
      }
    } catch (error) {
      return { success: false, message: 'Erro de conexão' };
    } finally {
      setLoading(false);
    }
  };

  const getCartItemsCount = () => {
    return cart.items?.reduce((total, item) => total + item.quantity, 0) || 0;
  };

  const value = {
    cart,
    loading,
    addToCart,
    updateCartItem,
    removeFromCart,
    checkout,
    getCartItemsCount,
    fetchCart,
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};

