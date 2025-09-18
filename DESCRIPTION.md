## 🎒 Loja Escolar - Sistema E-commerce

Sistema completo de e-commerce para produtos escolares desenvolvido com FastAPI e frontend responsivo.

### 🚀 Tecnologias
- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** HTML5 + CSS3 + JavaScript Vanilla
- **Autenticação:** JWT Tokens
- **Design:** Inspirado no Nubank

### 📦 Funcionalidades
- ✅ Catálogo de produtos
- ✅ Carrinho de compras
- ✅ Sistema de cupons
- ✅ Painel administrativo
- ✅ Autenticação segura
- ✅ Design responsivo

### 🎯 Como Executar
```bash
# Clonar repositório
git clone https://github.com/bl3ckz/dw2-PedroDantas-vendas.git

# Instalar dependências
cd dw2-PedroDantas-vendas
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt

# Executar seed e iniciar servidor
python backend/seed.py
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Acesse: http://127.0.0.1:8000 🚀