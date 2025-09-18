import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

# Adicionar o diretório backend ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, create_tables
from backend.models import User, Product, Coupon
from backend.security import hash_password

def create_seed_data():
    """Cria dados iniciais para o sistema"""
    
    # Criar tabelas se não existirem
    create_tables()
    
    # Obter sessão do banco
    db = SessionLocal()
    
    try:
        print("🌱 Iniciando seed do banco de dados...")
        
        # Criar usuário admin (idempotente)
        admin_email = "admin@lojaescolar.local"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if not existing_admin:
            admin_user = User(
                name="Administrador",
                email=admin_email,
                password_hash=hash_password("Admin123!")
            )
            db.add(admin_user)
            print(f"✅ Usuário admin criado: {admin_email}")
        else:
            print(f"ℹ️  Usuário admin já existe: {admin_email}")
        
        # Criar cupom ALUNO10 (idempotente)
        coupon_code = "ALUNO10"
        existing_coupon = db.query(Coupon).filter(Coupon.code == coupon_code).first()
        
        if not existing_coupon:
            coupon = Coupon(
                code=coupon_code,
                discount_percent=10,
                active=True,
                valid_until=datetime.utcnow() + timedelta(days=365)  # Válido por 1 ano
            )
            db.add(coupon)
            print(f"✅ Cupom criado: {coupon_code} (10% de desconto)")
        else:
            print(f"ℹ️  Cupom já existe: {coupon_code}")
        
        # Produtos escolares com imagens reais
        products_data = [
            {
                "name": "Caderno Espiral Universitário 200 Folhas",
                "description": "Caderno espiral universitário com 200 folhas, capa dura, ideal para anotações de aula.",
                "price": Decimal("15.90"),
                "stock": 50,
                "category": "Cadernos",
                "sku": "CAD-ESP-200",
                "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Mochila Escolar Juvenil",
                "description": "Mochila escolar resistente com múltiplos compartimentos, ideal para estudantes.",
                "price": Decimal("89.90"),
                "stock": 25,
                "category": "Mochilas",
                "sku": "MOCH-JUV-01",
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Kit Canetas Esferográficas Coloridas",
                "description": "Conjunto com 12 canetas esferográficas de cores variadas, escrita suave.",
                "price": Decimal("24.50"),
                "stock": 40,
                "category": "Canetas",
                "sku": "CAN-KIT-12",
                "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Estojo Escolar Duplo",
                "description": "Estojo escolar com dois compartimentos, perfeito para organizar material escolar.",
                "price": Decimal("32.90"),
                "stock": 30,
                "category": "Acessórios",
                "sku": "EST-DUP-01",
                "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Lápis HB - Caixa com 12 Unidades",
                "description": "Caixa com 12 lápis HB de excelente qualidade para escrita e desenho.",
                "price": Decimal("18.90"),
                "stock": 60,
                "category": "Acessórios",
                "sku": "LAP-HB-12",
                "image_url": "https://images.unsplash.com/photo-1590338819376-dd4c8ac19b7c?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Apontador com Depósito",
                "description": "Apontador metálico com depósito para aparas, qualidade premium.",
                "price": Decimal("8.50"),
                "stock": 45,
                "category": "Acessórios",
                "sku": "APT-DEP-01",
                "image_url": "https://images.unsplash.com/photo-1592439120213-ade4cae6b8c5?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Marca Texto Amarelo",
                "description": "Marca texto amarelo fluorescente, ideal para destacar textos importantes.",
                "price": Decimal("6.90"),
                "stock": 35,
                "category": "Canetas",
                "sku": "MRC-TXT-AM",
                "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Régua 30cm Transparente",
                "description": "Régua transparente de 30cm em acrílico resistente, graduação precisa.",
                "price": Decimal("4.50"),
                "stock": 55,
                "category": "Acessórios",
                "sku": "REG-30-TR",
                "image_url": "https://images.unsplash.com/photo-1582485574250-c3604c5b6e9b?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Borracha Escolar Branca",
                "description": "Borracha escolar branca macia, apaga sem danificar o papel.",
                "price": Decimal("2.90"),
                "stock": 80,
                "category": "Acessórios",
                "sku": "BOR-ESC-BR",
                "image_url": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Calculadora Científica",
                "description": "Calculadora científica com funções trigonométricas e logarítmicas.",
                "price": Decimal("45.90"),
                "stock": 20,
                "category": "Acessórios",
                "sku": "CALC-CIENT",
                "image_url": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Pasta com Elástico A4",
                "description": "Pasta organizadora A4 com elástico, ideal para manter documentos organizados.",
                "price": Decimal("12.90"),
                "stock": 35,
                "category": "Acessórios",
                "sku": "PAST-ELA-A4",
                "image_url": "https://images.unsplash.com/photo-1569243714807-4c28f990b4bf?w=800&h=600&fit=crop&crop=center"
            },
            {
                "name": "Caderno de Desenho A4",
                "description": "Caderno de desenho A4 com papel especial para arte e ilustração, 100 folhas.",
                "price": Decimal("22.90"),
                "stock": 25,
                "category": "Cadernos",
                "sku": "CAD-DES-A4",
                "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&h=600&fit=crop&crop=center"
            }
        ]
        
        # Criar produtos (idempotente por SKU)
        products_created = 0
        for product_data in products_data:
            existing_product = db.query(Product).filter(Product.sku == product_data["sku"]).first()
            
            if not existing_product:
                product = Product(**product_data)
                db.add(product)
                products_created += 1
        
        if products_created > 0:
            print(f"✅ {products_created} produtos criados")
        else:
            print("ℹ️  Produtos já existem no banco")
        
        # Salvar todas as alterações
        db.commit()
        print("🎉 Seed concluído com sucesso!")
        
        # Exibir informações importantes
        print("\n📋 Informações importantes:")
        print(f"👤 Usuário admin: {admin_email}")
        print(f"🔑 Senha admin: Admin123!")
        print(f"🎫 Cupom de desconto: {coupon_code} (10% off)")
        print(f"📦 Total de produtos disponíveis: {db.query(Product).count()}")
        print("\n✨ Sistema pronto para uso!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro durante o seed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()