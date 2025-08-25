import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.product import Product
from src.models.order import Order, OrderItem
from src.routes.user import user_bp
from src.routes.product import product_bp
from src.routes.order import order_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criar tabelas e dados de exemplo
with app.app_context():
    db.create_all()
    
    # Adicionar produtos de exemplo se não existirem
    if Product.query.count() == 0:
        sample_products = [
            Product(name='Smartphone Samsung Galaxy', description='Smartphone com tela de 6.1 polegadas, 128GB de armazenamento', price=899.99, image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300'),
            Product(name='Notebook Dell Inspiron', description='Notebook com processador Intel i5, 8GB RAM, SSD 256GB', price=2499.99, image='https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300'),
            Product(name='Fone de Ouvido Bluetooth', description='Fone sem fio com cancelamento de ruído', price=299.99, image='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300'),
            Product(name='Smart TV 55 polegadas', description='TV 4K com sistema Android TV integrado', price=1899.99, image='https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=300'),
            Product(name='Câmera Digital Canon', description='Câmera DSLR com lente 18-55mm', price=1599.99, image='https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=300'),
            Product(name='Tablet iPad Air', description='Tablet com tela de 10.9 polegadas, 64GB', price=1299.99, image='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300')
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()
        print("Produtos de exemplo adicionados ao banco de dados!")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
