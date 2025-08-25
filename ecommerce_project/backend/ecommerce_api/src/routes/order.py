from flask import Blueprint, jsonify, request
from src.models.order import Order, OrderItem
from src.models.product import Product
from src.models.user import db
from src.routes.user import token_required

order_bp = Blueprint('order', __name__)

@order_bp.route('/cart', methods=['POST'])
@token_required
def add_to_cart(current_user_id):
    """Adicionar produto ao carrinho (criar pedido pendente)"""
    data = request.json
    product_id = data['product_id']
    quantity = data.get('quantity', 1)
    
    # Verificar se o produto existe
    product = Product.query.get_or_404(product_id)
    
    # Buscar pedido pendente do usuário ou criar um novo
    order = Order.query.filter_by(user_id=current_user_id, status='pending').first()
    if not order:
        order = Order(user_id=current_user_id, status='pending')
        db.session.add(order)
        db.session.flush()  # Para obter o ID do pedido
    
    # Verificar se o item já existe no carrinho
    order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()
    if order_item:
        order_item.quantity += quantity
    else:
        order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Produto adicionado ao carrinho',
        'cart': order.to_dict()
    }), 201

@order_bp.route('/cart', methods=['GET'])
@token_required
def get_cart(current_user_id):
    """Obter carrinho do usuário"""
    order = Order.query.filter_by(user_id=current_user_id, status='pending').first()
    if not order:
        return jsonify({'cart': {'items': [], 'total': 0}})
    
    # Calcular total
    total = sum(item.product.price * item.quantity for item in order.items)
    
    cart_data = order.to_dict()
    cart_data['total'] = total
    
    return jsonify({'cart': cart_data})

@order_bp.route('/cart/item/<int:product_id>', methods=['PUT'])
@token_required
def update_cart_item(current_user_id, product_id):
    """Atualizar quantidade de item no carrinho"""
    data = request.json
    quantity = data['quantity']
    
    order = Order.query.filter_by(user_id=current_user_id, status='pending').first()
    if not order:
        return jsonify({'message': 'Carrinho não encontrado'}), 404
    
    order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()
    if not order_item:
        return jsonify({'message': 'Item não encontrado no carrinho'}), 404
    
    if quantity <= 0:
        db.session.delete(order_item)
    else:
        order_item.quantity = quantity
    
    db.session.commit()
    
    return jsonify({
        'message': 'Item atualizado',
        'cart': order.to_dict()
    })

@order_bp.route('/cart/item/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user_id, product_id):
    """Remover item do carrinho"""
    order = Order.query.filter_by(user_id=current_user_id, status='pending').first()
    if not order:
        return jsonify({'message': 'Carrinho não encontrado'}), 404
    
    order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()
    if not order_item:
        return jsonify({'message': 'Item não encontrado no carrinho'}), 404
    
    db.session.delete(order_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Item removido do carrinho',
        'cart': order.to_dict()
    })

@order_bp.route('/checkout', methods=['POST'])
@token_required
def checkout(current_user_id):
    """Finalizar pedido"""
    order = Order.query.filter_by(user_id=current_user_id, status='pending').first()
    if not order or not order.items:
        return jsonify({'message': 'Carrinho vazio'}), 400
    
    # Alterar status do pedido para 'completed'
    order.status = 'completed'
    db.session.commit()
    
    # Calcular total
    total = sum(item.product.price * item.quantity for item in order.items)
    
    return jsonify({
        'message': 'Pedido finalizado com sucesso',
        'order': order.to_dict(),
        'total': total
    })

@order_bp.route('/orders', methods=['GET'])
@token_required
def get_user_orders(current_user_id):
    """Obter pedidos do usuário"""
    orders = Order.query.filter_by(user_id=current_user_id).filter(Order.status != 'pending').all()
    
    orders_data = []
    for order in orders:
        order_data = order.to_dict()
        order_data['total'] = sum(item.product.price * item.quantity for item in order.items)
        orders_data.append(order_data)
    
    return jsonify({'orders': orders_data})

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order(current_user_id, order_id):
    """Obter um pedido específico"""
    order = Order.query.filter_by(id=order_id, user_id=current_user_id).first_or_404()
    
    order_data = order.to_dict()
    order_data['total'] = sum(item.product.price * item.quantity for item in order.items)
    
    return jsonify({'order': order_data})

