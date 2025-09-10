from src.main import app
from src.models.product import Product
from src.models.user import db

# Lista de produtos escolares
produtos_escolares = [
    {
        "name": "Kit Cadernos Universitários",
        "description": "Kit com 10 cadernos universitários, capa dura, 96 folhas, pautados",
        "price": 299.99,
        "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?w=500&h=500&fit=crop"
    },
    {
        "name": "Mochila Escolar Premium",
        "description": "Mochila escolar ergonômica com compartimento para laptop e diversos bolsos",
        "price": 899.99,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop"
    },
    {
        "name": "Estojo Completo",
        "description": "Estojo escolar completo com 50 itens incluindo lápis, canetas, borrachas e mais",
        "price": 199.99,
        "image": "https://images.unsplash.com/photo-1596468138858-dc22459cd760?w=500&h=500&fit=crop"
    },
    {
        "name": "Kit Arte Profissional",
        "description": "Kit de arte com tintas, pincéis, lápis de cor e materiais para desenho",
        "price": 1899.99,
        "image": "https://images.unsplash.com/photo-1605711285791-0219e80e43a3?w=500&h=500&fit=crop"
    },
    {
        "name": "Calculadora Científica HP 10s+",
        "description": "Calculadora científica HP com display de 2 linhas, funções estatísticas e científicas",
        "price": 1599.99,
        "image": "https://www.hpstore.com.br/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/c/a/calculadora-cientifica-hp-10s-2.jpg"
    },
    {
        "name": "Mesa Digitalizadora",
        "description": "Mesa digitalizadora para aulas de arte e desenho digital",
        "price": 1299.99,
        "image": "https://images.unsplash.com/photo-1589135364686-82ce0a12e7b6?w=500&h=500&fit=crop"
    }
]

with app.app_context():
    # Limpa todos os produtos existentes
    Product.query.delete()
    
    # Adiciona os novos produtos
    for produto in produtos_escolares:
        new_product = Product(
            name=produto["name"],
            description=produto["description"],
            price=produto["price"],
            image=produto["image"]
        )
        db.session.add(new_product)
    
    db.session.commit()
    print("Produtos atualizados com sucesso!")
