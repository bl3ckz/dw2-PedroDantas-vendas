from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator

# Schemas de Usuário
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email válido")
    password: str = Field(..., min_length=6, description="Senha com mínimo 6 caracteres")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas de Produto
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, description="Nome do produto")
    description: Optional[str] = Field(None, description="Descrição do produto")
    price: Decimal = Field(..., ge=Decimal('0.01'), description="Preço deve ser maior que 0")
    stock: int = Field(..., ge=0, description="Estoque não pode ser negativo")
    category: str = Field(..., description="Categoria obrigatória")
    sku: Optional[str] = Field(None, max_length=100, description="SKU único")
    image_url: Optional[str] = Field(None, max_length=500, description="URL da imagem")
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v.quantize(Decimal('0.01'))

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=60)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=Decimal('0.01'))
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)
    
    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v.quantize(Decimal('0.01')) if v else v

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: str  # Decimal serializado como string
    stock: int
    category: str
    sku: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schemas de Paginação
class ProductsListResponse(BaseModel):
    data: List[ProductResponse]
    meta: dict

# Schemas de Cupom
class CouponValidateResponse(BaseModel):
    valid: bool
    discount_percent: int
    code: str
    message: Optional[str] = None

# Schemas de Pedido
class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., ge=1, description="Quantidade deve ser pelo menos 1")

class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Lista de itens do pedido")
    coupon_code: Optional[str] = Field(None, description="Código do cupom")

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: str
    line_total: str
    product: ProductResponse
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: Optional[int]
    subtotal: str
    discount_amount: str
    total_final: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

# Schemas de Autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None