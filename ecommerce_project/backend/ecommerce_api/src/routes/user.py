from flask import Blueprint, jsonify, request
from src.models.user import User, db
import jwt
from functools import wraps
import datetime

user_bp = Blueprint('user', __name__)

# Função para gerar token JWT
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, 'asdf#FGSgvasgf$5$WGT', algorithm='HS256')

# Decorator para verificar token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token é necessário'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, 'asdf#FGSgvasgf$5$WGT', algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

@user_bp.route('/register', methods=['POST'])
def register():
    """Cadastro de usuário"""
    data = request.json
    
    # Verificar se o email já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email já cadastrado'}), 400
    
    # Criar novo usuário
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Gerar token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Usuário cadastrado com sucesso',
        'token': token,
        'user': user.to_dict()
    }), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    data = request.json
    
    # Buscar usuário pelo email
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Email ou senha incorretos'}), 401
    
    # Gerar token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': user.to_dict()
    }), 200

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    """Obter perfil do usuário logado"""
    user = User.query.get_or_404(current_user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user_id, user_id):
    # Usuário só pode atualizar seu próprio perfil
    if current_user_id != user_id:
        return jsonify({'message': 'Não autorizado'}), 403
        
    user = User.query.get_or_404(user_id)
    data = request.json
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user_id, user_id):
    # Usuário só pode deletar seu próprio perfil
    if current_user_id != user_id:
        return jsonify({'message': 'Não autorizado'}), 403
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
