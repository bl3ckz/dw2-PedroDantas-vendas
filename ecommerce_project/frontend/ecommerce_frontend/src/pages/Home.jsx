import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowRight, ShoppingBag, Truck, Shield, CreditCard } from 'lucide-react';
import ProductCard from '../components/ProductCard';

const Home = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedProducts();
  }, []);

  const fetchFeaturedProducts = async () => {
    try {
      const response = await fetch('/api/products');
      if (response.ok) {
        const products = await response.json();
        // Pegar apenas os primeiros 4 produtos como destaque
        setFeaturedProducts(products.slice(0, 4));
      }
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Bem-vindo à TechStore
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
            Sua loja online de tecnologia com os melhores produtos e preços incríveis
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/products">
              <Button size="lg" variant="secondary" className="text-lg px-8">
                Ver Produtos
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Por que escolher a TechStore?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center p-6">
              <CardContent className="pt-6">
                <Truck className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Entrega Rápida</h3>
                <p className="text-gray-600">
                  Entregamos seus produtos com rapidez e segurança
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center p-6">
              <CardContent className="pt-6">
                <Shield className="h-12 w-12 text-green-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Compra Segura</h3>
                <p className="text-gray-600">
                  Seus dados estão protegidos com nossa segurança avançada
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center p-6">
              <CardContent className="pt-6">
                <CreditCard className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Pagamento Fácil</h3>
                <p className="text-gray-600">
                  Múltiplas formas de pagamento para sua comodidade
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-3xl font-bold">Produtos em Destaque</h2>
            <Link to="/products">
              <Button variant="outline">
                Ver Todos
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
          
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, index) => (
                <Card key={index} className="animate-pulse">
                  <div className="aspect-square bg-gray-200 rounded-t-lg"></div>
                  <CardContent className="p-4">
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded mb-3"></div>
                    <div className="h-6 bg-gray-200 rounded"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {featuredProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gray-900 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <ShoppingBag className="h-16 w-16 text-blue-400 mx-auto mb-6" />
          <h2 className="text-3xl font-bold mb-4">
            Pronto para começar suas compras?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Cadastre-se agora e aproveite ofertas exclusivas em nossa loja
          </p>
          <Link to="/register">
            <Button size="lg" className="text-lg px-8">
              Criar Conta Grátis
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;

