from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime

from backend.database import get_db, create_tables
from backend.models import User, Product, Coupon, Order, OrderItem
from backend.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    ProductCreate, ProductUpdate, ProductResponse, ProductsListResponse,
    CouponValidateResponse, OrderCreate, OrderResponse
)
from backend.security import (
    hash_password, authenticate_user, create_access_token, get_current_user
)

# Criar tabelas
create_tables()

# Instanciar FastAPI
app = FastAPI(
    title="Loja Escolar API",
    description="API para e-commerce de produtos escolares",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Utilitários
def serialize_decimal(value: Decimal) -> str:
    """Serializa Decimal para string"""
    return str(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

# Rotas de Autenticação
@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verificar se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado no sistema"
        )
    
    # Criar novo usuário
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas de Produtos
@app.get("/products", response_model=ProductsListResponse)
async def list_products(
    search: Optional[str] = Query(None, description="Buscar por nome"),
    sort: Optional[str] = Query("name", pattern="^(price|name)$", description="Ordenar por price ou name"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$", description="Ordem asc ou desc"),
    page: int = Query(1, ge=1, description="Página"),
    page_size: int = Query(12, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db)
):
    # Query base
    query = db.query(Product)
    
    # Aplicar busca
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(func.lower(Product.name).like(search_term))
    
    # Contar total
    total = query.count()
    
    # Aplicar ordenação
    if sort == "price":
        if order == "desc":
            query = query.order_by(Product.price.desc())
        else:
            query = query.order_by(Product.price.asc())
    else:  # sort == "name"
        if order == "desc":
            query = query.order_by(Product.name.desc())
        else:
            query = query.order_by(Product.name.asc())
    
    # Aplicar paginação
    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()
    
    # Serializar produtos
    products_data = []
    for product in products:
        product_dict = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": serialize_decimal(product.price),
            "stock": product.stock,
            "category": product.category,
            "sku": product.sku,
            "image_url": product.image_url,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        products_data.append(product_dict)
    
    return {
        "data": products_data,
        "meta": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "sort": sort,
            "order": order,
            "search": search
        }
    }

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": serialize_decimal(product.price),
        "stock": product.stock,
        "category": product.category,
        "sku": product.sku,
        "image_url": product.image_url,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar SKU único se fornecido
    if product_data.sku:
        existing_sku = db.query(Product).filter(Product.sku == product_data.sku).first()
        if existing_sku:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SKU já existe no sistema"
            )
    
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category,
        sku=product_data.sku,
        image_url=product_data.image_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": serialize_decimal(product.price),
        "stock": product.stock,
        "category": product.category,
        "sku": product.sku,
        "image_url": product.image_url,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    # Verificar SKU único se alterado
    if product_data.sku and product_data.sku != product.sku:
        existing_sku = db.query(Product).filter(Product.sku == product_data.sku).first()
        if existing_sku:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SKU já existe no sistema"
            )
    
    # Atualizar campos fornecidos
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": serialize_decimal(product.price),
        "stock": product.stock,
        "category": product.category,
        "sku": product.sku,
        "image_url": product.image_url,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    db.delete(product)
    db.commit()

# Rotas de Cupom
@app.get("/coupons/{code}/validate", response_model=CouponValidateResponse)
async def validate_coupon(code: str, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(
        func.lower(Coupon.code) == code.lower(),
        Coupon.active == True
    ).first()
    
    if not coupon:
        return {
            "valid": False,
            "discount_percent": 0,
            "code": code,
            "message": "Cupom não encontrado ou inativo"
        }
    
    # Verificar expiração
    if coupon.valid_until and coupon.valid_until < datetime.utcnow():
        return {
            "valid": False,
            "discount_percent": 0,
            "code": code,
            "message": "Cupom expirado"
        }
    
    return {
        "valid": True,
        "discount_percent": coupon.discount_percent,
        "code": coupon.code,
        "message": "Cupom válido"
    }

# Rotas de Pedido
@app.post("/orders/confirm", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def confirm_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        # Iniciar transação
        # Validar produtos e calcular subtotal
        subtotal = Decimal('0.00')
        order_items_data = []
        
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto com ID {item.product_id} não encontrado"
                )
            
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Estoque insuficiente para {product.name}. Disponível: {product.stock}, solicitado: {item.quantity}"
                )
            
            if product.stock == 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Produto {product.name} está fora de estoque"
                )
            
            line_total = product.price * item.quantity
            subtotal += line_total
            
            order_items_data.append({
                "product": product,
                "quantity": item.quantity,
                "unit_price": product.price,
                "line_total": line_total
            })
        
        # Aplicar cupom se fornecido
        discount_amount = Decimal('0.00')
        if order_data.coupon_code:
            coupon = db.query(Coupon).filter(
                func.lower(Coupon.code) == order_data.coupon_code.lower(),
                Coupon.active == True
            ).first()
            
            if coupon and (not coupon.valid_until or coupon.valid_until > datetime.utcnow()):
                discount_amount = (subtotal * Decimal(str(coupon.discount_percent)) / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Calcular total final
        total_final = (subtotal - discount_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Criar pedido
        order = Order(
            user_id=None,  # Permitir pedido sem login
            subtotal=subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            discount_amount=discount_amount,
            total_final=total_final
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # Criar itens do pedido e reduzir estoque
        order_items = []
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                line_total=item_data["line_total"]
            )
            db.add(order_item)
            
            # Reduzir estoque
            item_data["product"].stock -= item_data["quantity"]
            
            order_items.append(order_item)
        
        db.commit()
        
        # Buscar pedido completo com relacionamentos
        order_complete = db.query(Order).filter(Order.id == order.id).first()
        
        # Preparar resposta
        items_response = []
        for item in order_complete.items:
            items_response.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": serialize_decimal(item.unit_price),
                "line_total": serialize_decimal(item.line_total),
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "description": item.product.description,
                    "price": serialize_decimal(item.product.price),
                    "stock": item.product.stock,
                    "category": item.product.category,
                    "sku": item.product.sku,
                    "image_url": item.product.image_url,
                    "created_at": item.product.created_at,
                    "updated_at": item.product.updated_at
                }
            })
        
        return {
            "id": order_complete.id,
            "user_id": order_complete.user_id,
            "subtotal": serialize_decimal(order_complete.subtotal),
            "discount_amount": serialize_decimal(order_complete.discount_amount),
            "total_final": serialize_decimal(order_complete.total_final),
            "created_at": order_complete.created_at,
            "items": items_response
        }
        
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao confirmar pedido"
        )

# Rota raiz
@app.get("/")
async def root():
    return {"message": "Loja Escolar API - Sistema funcionando"}

# Executar servidor se executado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)