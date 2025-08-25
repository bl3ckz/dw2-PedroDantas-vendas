from flask import Blueprint, jsonify, request
from src.models.product import Product
from src.models.user import db
from src.routes.user import token_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    """Listar todos os produtos"""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obter um produto específico"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@product_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user_id):
    """Criar um novo produto (apenas usuários autenticados)"""
    data = request.json
    
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        image=data.get('image', '')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'message': 'Produto criado com sucesso',
        'product': product.to_dict()
    }), 201

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(current_user_id, product_id):
    """Atualizar um produto (apenas usuários autenticados)"""
    product = Product.query.get_or_404(product_id)
    data = request.json
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image = data.get('image', product.image)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Produto atualizado com sucesso',
        'product': product.to_dict()
    })

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user_id, product_id):
    """Deletar um produto (apenas usuários autenticados)"""
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Produto deletado com sucesso'}), 204

