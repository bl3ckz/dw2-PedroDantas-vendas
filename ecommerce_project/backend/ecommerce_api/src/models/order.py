from src.models.user import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')
    
    # Relacionamento com usuário
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    
    # Relacionamento com itens do pedido
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relacionamento com produto
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return f'<OrderItem order_id={self.order_id} product_id={self.product_id}>'

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None
        }

