# 🎒 Loja Escolar - E-commerce de Produtos Escolares

![Versão](https://img.shields.io/badge/versão-1.0.0-purple)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green)
![Status](https://img.shields.io/badge/status-pronto-brightgreen)

> Sistema completo de e-commerce para produtos escolares com design moderno e funcionalidades avançadas.

## 📖 Visão Geral

A **Loja Escolar** é um sistema completo de e-commerce desenvolvido especificamente para a venda de produtos escolares. O projeto implementa um catálogo online com carrinho de compras, sistema de cupons de desconto e painel administrativo, seguindo as melhores práticas de desenvolvimento web.

### ✨ Características Principais

- **Interface Moderna**: Design inspirado no Nubank com paleta roxa/lilás
- **Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Acessível**: Conformidade com WCAG AA para acessibilidade
- **Internacionalizado**: 100% em português brasileiro (pt-BR)
- **Funcional**: Sistema completo de carrinho e cupons funcionais

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+** - Linguagem principal
- **FastAPI 0.115.0** - Framework web moderno e rápido
- **SQLAlchemy 2.0.34** - ORM para banco de dados
- **SQLite** - Banco de dados (arquivo app.db)
- **Pydantic 2.9.2** - Validação de dados
- **passlib[bcrypt]** - Hash de senhas
- **python-jose** - Autenticação JWT
- **uvicorn** - Servidor ASGI

### Frontend
- **HTML5** - Estrutura semântica
- **CSS3** - Estilos com Flexbox/Grid
- **JavaScript ES6+** - Interatividade (vanilla JS)
- **Design System** - Paleta inspirada no Nubank

## 🎨 Design e UX

### Paleta de Cores (Inspirada no Nubank)
- **Roxo Primário**: `#820AD1` - Botões principais e destaques
- **Roxo Escuro**: `#6F08AA` - Estados hover e foco
- **Lilás Claro**: `#EEDCFF` - Fundos suaves e chips
- **Verde Sucesso**: `#1DB954` - Confirmações e cupons aplicados
- **Vermelho Erro**: `#E53935` - Alertas e validações
- **Cinzas Neutros**: Hierarquia de textos e bordas

### Acessibilidade
- ✅ Contraste WCAG AA (mínimo 4.5:1)
- ✅ Navegação por teclado completa
- ✅ ARIA labels e roles apropriados
- ✅ Foco visível em todos os elementos interativos
- ✅ Textos alternativos descritivos
- ✅ Suporte a leitores de tela

## 📁 Estrutura do Projeto

```
dw2_pedro_vendas/
├── backend/
│   ├── app.py              # Aplicação FastAPI principal
│   ├── database.py         # Configuração do banco SQLite
│   ├── models.py           # Modelos SQLAlchemy
│   ├── schemas.py          # Schemas Pydantic para validação
│   ├── security.py         # Autenticação JWT e hash de senhas
│   ├── seed.py             # Dados iniciais (usuários, produtos, cupons)
│   ├── requirements.txt    # Dependências Python
│   └── app.db             # Banco SQLite (criado após seed)
├── frontend/
│   ├── index.html         # Página principal (catálogo)
│   ├── admin.html         # Painel administrativo
│   ├── login.html         # Página de login
│   ├── register.html      # Página de cadastro
│   ├── styles.css         # Estilos CSS com paleta Nubank
│   ├── scripts.js         # JavaScript da aplicação
│   └── assets/            # Imagens (referências via URLs)
├── README.md              # Este arquivo
├── REPORT.md              # Relatório técnico detalhado
└── ChatIA.md              # Registro de desenvolvimento via IA
```

## 🚀 Instalação e Execução

### Pré-requisitos
- **Python 3.11 ou superior**
- **pip** (gerenciador de pacotes Python)
- **VS Code** com extensão Live Server (recomendado)

### 1. Configurar Ambiente Virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r backend/requirements.txt
```

### 3. Criar Banco de Dados e Dados Iniciais
```bash
python backend/seed.py
```

### 4. Executar o Backend

**Opção 1 - FastAPI Dev (Recomendado):**
```bash
fastapi dev backend/app.py
```

**Opção 2 - Uvicorn:**
```bash
uvicorn backend.app:app --reload
```

**Opção 3 - Python direto:**
```bash
python backend/app.py
```

O backend estará disponível em: http://127.0.0.1:8000

### 5. Executar o Frontend

**Opção 1 - VS Code Live Server:**
1. Abra a pasta `/frontend` no VS Code
2. Clique com botão direito em `index.html`
3. Selecione "Open with Live Server"

**Opção 2 - Servidor HTTP Python:**
```bash
cd frontend
python -m http.server 5500
```

O frontend estará disponível em: http://127.0.0.1:5500

## 👤 Dados de Acesso

### Usuário Administrador
- **E-mail**: `admin@lojaescolar.local`
- **Senha**: `Admin123!`

### Cupom de Desconto
- **Código**: `ALUNO10`
- **Desconto**: 10% sobre o subtotal
- **Status**: Ativo por 1 ano

## 🔗 API Endpoints

### Base URL: `http://127.0.0.1:8000`

### Autenticação
```bash
# Registrar usuário
POST /auth/register
Content-Type: application/json
{
  "name": "Nome do Usuário",
  "email": "usuario@email.com",
  "password": "senha123"
}

# Login
POST /auth/login
Content-Type: application/json
{
  "email": "admin@lojaescolar.local",
  "password": "Admin123!"
}
```

### Produtos
```bash
# Listar produtos
GET /products?search=caderno&sort=price&order=asc&page=1&page_size=12

# Obter produto específico
GET /products/{id}

# Criar produto (requer autenticação)
POST /products
Authorization: Bearer {token}
Content-Type: application/json
{
  "name": "Produto Teste",
  "description": "Descrição do produto",
  "price": 19.90,
  "stock": 50,
  "category": "Acessórios",
  "sku": "PROD-001",
  "image_url": "https://exemplo.com/imagem.jpg"
}

# Atualizar produto (requer autenticação)
PUT /products/{id}
Authorization: Bearer {token}

# Excluir produto (requer autenticação)
DELETE /products/{id}
Authorization: Bearer {token}
```

### Cupons
```bash
# Validar cupom
GET /coupons/ALUNO10/validate
```

### Pedidos
```bash
# Confirmar pedido
POST /orders/confirm
Content-Type: application/json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ],
  "coupon_code": "ALUNO10"
}
```

## ⚙️ Configuração

### Variáveis de Ambiente (Opcionais)
```bash
JWT_SECRET=sua_chave_secreta_super_segura
JWT_ALGO=HS256
JWT_EXPIRES_MIN=120
```

### CORS
A API está configurada para aceitar requisições de:
- `http://127.0.0.1:5500`
- `http://localhost:5500`
- `http://127.0.0.1:3000`
- `http://localhost:3000`
- `http://127.0.0.1:5173`
- `http://localhost:5173`
- `http://127.0.0.1:8000`
- `http://localhost:8000`

## 💳 Sistema de Preços

- **Moeda**: Real Brasileiro (BRL)
- **Formato**: R$ 0.000,00
- **Precisão**: 2 casas decimais
- **Cálculos**: Usando Decimal para precisão financeira
- **Arredondamento**: ROUND_HALF_UP

## 🛒 Funcionalidades do Sistema

### Catálogo de Produtos
- ✅ Listagem responsiva em grid
- ✅ Busca por nome com debounce (300ms)
- ✅ Ordenação por preço e nome (asc/desc)
- ✅ Paginação server-side
- ✅ Imagens reais dos produtos
- ✅ Indicação de estoque

### Carrinho de Compras
- ✅ Persistência no localStorage
- ✅ Badge com quantidade sincronizada
- ✅ Drawer/modal acessível
- ✅ Controle de quantidade com validação de estoque
- ✅ Remoção de itens
- ✅ Cálculo de subtotal em tempo real

### Sistema de Cupons
- ✅ Aplicação do cupom "ALUNO10" (10% off)
- ✅ Validação case-insensitive
- ✅ Verificação de validade no backend
- ✅ Remoção de cupom aplicado
- ✅ Cálculo correto de desconto

### Finalização de Pedido
- ✅ Validação de estoque em tempo real
- ✅ Transação atômica (rollback em erro)
- ✅ Redução automática de estoque
- ✅ Aplicação de desconto de cupom
- ✅ Geração de número do pedido

### Painel Administrativo
- ✅ Autenticação obrigatória (JWT)
- ✅ CRUD completo de produtos
- ✅ Formulário com validações HTML5 + JS
- ✅ Upload de imagem via URL
- ✅ Feedback visual de operações

## 🔍 Créditos de Imagens

Todas as imagens dos produtos são obtidas de fontes públicas:

- **Unsplash** - Imagens gratuitas de alta qualidade
  - Cadernos: https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c
  - Mochilas: https://images.unsplash.com/photo-1553062407-98eeb64c6a62
  - Canetas: https://images.unsplash.com/photo-1586953208448-b95a79798f07
  - Outros produtos escolares de uso educacional

## 🧪 Testes Manuais

### Fluxo Completo de Compra
1. **Navegação**: Acessar catálogo e buscar produtos
2. **Carrinho**: Adicionar produtos respeitando estoque
3. **Cupom**: Aplicar "ALUNO10" e verificar desconto
4. **Pedido**: Finalizar e verificar redução de estoque
5. **Admin**: Login e verificar produtos atualizados

### Testes de Validação
1. **Produtos**: Tentar criar com preço inválido (< 0.01)
2. **Estoque**: Verificar bloqueio quando estoque = 0
3. **Cupom**: Testar códigos inválidos e expirados
4. **Auth**: Verificar proteção de rotas administrativas

### Testes de Acessibilidade
1. **Teclado**: Navegar usando apenas Tab e Enter
2. **Screen Reader**: Verificar leitura de elementos
3. **Contraste**: Validar legibilidade em diferentes temas
4. **Foco**: Verificar indicadores visuais de foco

## 🐛 Resolução de Problemas

### Backend não inicia
```bash
# Verificar se o Python está instalado corretamente
python --version

# Reinstalar dependências
pip install -r backend/requirements.txt --force-reinstall

# Verificar se as tabelas foram criadas
python backend/seed.py
```

### Frontend não carrega produtos
1. Verificar se o backend está rodando em http://127.0.0.1:8000
2. Verificar console do navegador para erros de CORS
3. Confirmar que `API_BASE` em scripts.js está correto

### Erro de autenticação
1. Verificar se o token JWT não expirou (padrão: 2 horas)
2. Limpar localStorage: `localStorage.clear()`
3. Fazer login novamente

## 📋 Checklist de Funcionalidades

### ✅ Requisitos Atendidos
- [x] Sistema completo em pt-BR
- [x] Paleta inspirada no Nubank
- [x] Backend FastAPI com SQLAlchemy
- [x] Frontend HTML/CSS/JS vanilla
- [x] Carrinho persistente no localStorage
- [x] Sistema de cupons funcionais
- [x] CRUD administrativo protegido
- [x] Validações client e server-side
- [x] Acessibilidade WCAG AA
- [x] Design responsivo
- [x] Imagens reais dos produtos
- [x] Documentação completa

### 🎯 Diferenciais Implementados
- [x] Debounce na busca para melhor performance
- [x] Loading states e feedback visual
- [x] Validação de estoque em tempo real
- [x] Transações atômicas no banco
- [x] Gerenciamento de estado centralizado
- [x] Suporte a atalhos de teclado (ESC para fechar modal)
- [x] Formatação monetária nativa (Intl.NumberFormat)
- [x] Arquitetura modular e escalável

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar este README.md
2. Consultar REPORT.md para detalhes técnicos
3. Revisar ChatIA.md para histórico de desenvolvimento

---

**Desenvolvido com ❤️ para educação**

*Sistema de e-commerce educacional - Loja Escolar v1.0.0*