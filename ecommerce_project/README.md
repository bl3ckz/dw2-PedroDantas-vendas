# TechStore - E-commerce Educacional

Um projeto completo de e-commerce desenvolvido para fins educacionais no ensino técnico, demonstrando a integração entre frontend e backend com funcionalidades essenciais de uma loja online.

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como trabalho escolar para demonstrar conceitos de desenvolvimento web full-stack, incluindo:

- **Frontend responsivo** com React e TailwindCSS
- **Backend robusto** com Flask e SQLAlchemy
- **Banco de dados** SQLite para persistência
- **Sistema de autenticação** com sessões
- **API REST** para comunicação frontend-backend
- **Carrinho de compras** funcional
- **Sistema de pedidos** simulado

## 🚀 Tecnologias Utilizadas

### Frontend
- **React 18** - Biblioteca JavaScript para interfaces
- **React Router** - Navegação entre páginas
- **TailwindCSS** - Framework CSS utilitário
- **Vite** - Build tool e servidor de desenvolvimento
- **Context API** - Gerenciamento de estado global

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **Flask-CORS** - Habilitação de CORS
- **Werkzeug** - Utilitários para hash de senhas
- **SQLite** - Banco de dados relacional

## 📁 Estrutura do Projeto

```
ecommerce_project/
├── backend/
│   └── ecommerce_api/
│       ├── src/
│       │   ├── models/          # Modelos do banco de dados
│       │   ├── routes/          # Rotas da API
│       │   ├── database/        # Configuração do banco
│       │   └── main.py          # Arquivo principal
│       ├── venv/                # Ambiente virtual Python
│       └── requirements.txt     # Dependências Python
└── frontend/
    └── ecommerce_frontend/
        ├── src/
        │   ├── components/      # Componentes React
        │   ├── contexts/        # Contextos React
        │   ├── pages/           # Páginas da aplicação
        │   └── main.jsx         # Arquivo principal
        ├── public/              # Arquivos estáticos
        └── package.json         # Dependências Node.js
```

## 🗄️ Banco de Dados

O projeto utiliza SQLite com as seguintes tabelas:

### Usuários (users)
- `id` - Chave primária
- `name` - Nome completo
- `email` - Email único
- `password_hash` - Senha criptografada

### Produtos (products)
- `id` - Chave primária
- `name` - Nome do produto
- `description` - Descrição
- `price` - Preço
- `image_url` - URL da imagem

### Pedidos (orders)
- `id` - Chave primária
- `user_id` - Referência ao usuário
- `created_at` - Data de criação
- `status` - Status do pedido
- `total` - Valor total

### Itens do Pedido (order_items)
- `id` - Chave primária
- `order_id` - Referência ao pedido
- `product_id` - Referência ao produto
- `quantity` - Quantidade
- `price` - Preço unitário

## 🔧 Como Executar

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- npm ou pnpm

### Backend
```bash
cd backend/ecommerce_api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
python src/main.py
```

### Frontend
```bash
cd frontend/ecommerce_frontend
pnpm install
pnpm run dev
```

### Acesso
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 🌟 Funcionalidades

### ✅ Implementadas
- [x] Página inicial com produtos em destaque
- [x] Catálogo completo de produtos
- [x] Sistema de cadastro e login
- [x] Autenticação por sessão
- [x] Carrinho de compras funcional
- [x] Adicionar/remover produtos do carrinho
- [x] Finalização de pedidos
- [x] Design responsivo (mobile-first)
- [x] Navegação intuitiva
- [x] Validação de formulários
- [x] Feedback visual para ações

### 🎯 Características Educacionais
- Código bem comentado e organizado
- Separação clara entre frontend e backend
- Uso de boas práticas de desenvolvimento
- Arquitetura REST para APIs
- Gerenciamento de estado com Context API
- Responsividade com TailwindCSS
- Validação tanto no frontend quanto backend

## 📱 Páginas da Aplicação

1. **Home** (`/`) - Página inicial com produtos em destaque
2. **Produtos** (`/products`) - Catálogo completo
3. **Login** (`/login`) - Autenticação de usuários
4. **Cadastro** (`/register`) - Registro de novos usuários
5. **Carrinho** (`/cart`) - Visualização e gestão do carrinho

## 🔐 Sistema de Autenticação

- Cadastro com validação de email único
- Login com email e senha
- Senhas criptografadas com Werkzeug
- Sessões persistentes
- Proteção de rotas que requerem autenticação
- Logout funcional

## 🛒 Fluxo de Compras

1. **Navegação** - Usuário explora produtos
2. **Seleção** - Adiciona produtos ao carrinho
3. **Autenticação** - Login obrigatório para comprar
4. **Carrinho** - Revisão dos itens selecionados
5. **Finalização** - Simulação de checkout
6. **Confirmação** - Pedido registrado no sistema

## 📊 API Endpoints

### Usuários
- `POST /api/register` - Cadastro de usuário
- `POST /api/login` - Login
- `POST /api/logout` - Logout
- `GET /api/profile` - Perfil do usuário

### Produtos
- `GET /api/products` - Listar produtos
- `GET /api/products/<id>` - Produto específico

### Carrinho
- `GET /api/cart` - Itens do carrinho
- `POST /api/cart` - Adicionar item
- `PUT /api/cart/<id>` - Atualizar quantidade
- `DELETE /api/cart/<id>` - Remover item

### Pedidos
- `POST /api/orders` - Criar pedido
- `GET /api/orders` - Histórico de pedidos

## 🎨 Design e UX

- **Cores**: Paleta azul e laranja moderna
- **Tipografia**: Fontes legíveis e hierarquia clara
- **Layout**: Grid responsivo com breakpoints
- **Componentes**: Cards, botões e formulários consistentes
- **Feedback**: Loading states e mensagens de erro/sucesso
- **Acessibilidade**: Contraste adequado e navegação por teclado

## 📚 Conceitos Demonstrados

### Frontend
- Componentes funcionais React
- Hooks (useState, useEffect, useContext)
- Roteamento com React Router
- Gerenciamento de estado global
- Comunicação com APIs
- Responsividade mobile-first

### Backend
- Arquitetura MVC
- APIs RESTful
- ORM com SQLAlchemy
- Autenticação e autorização
- Validação de dados
- Tratamento de erros
- CORS para integração

### Banco de Dados
- Modelagem relacional
- Chaves primárias e estrangeiras
- Relacionamentos entre tabelas
- Migrações automáticas

## 🔍 Testes Realizados

- ✅ Cadastro de usuários
- ✅ Login e logout
- ✅ Listagem de produtos
- ✅ Adição ao carrinho
- ✅ Remoção do carrinho
- ✅ Finalização de pedidos
- ✅ Responsividade mobile
- ✅ Navegação entre páginas
- ✅ Validações de formulário
- ✅ Tratamento de erros

## 🎓 Objetivos Educacionais Alcançados

1. **Desenvolvimento Full-Stack** - Integração completa frontend-backend
2. **Arquitetura Web** - Separação de responsabilidades
3. **Banco de Dados** - Modelagem e relacionamentos
4. **APIs REST** - Comunicação padronizada
5. **Autenticação** - Segurança básica
6. **UX/UI** - Interface intuitiva e responsiva
7. **Boas Práticas** - Código limpo e documentado

## 📝 Notas para Avaliação

Este projeto demonstra competências em:
- Programação frontend (React/JavaScript)
- Programação backend (Python/Flask)
- Banco de dados (SQLite/SQL)
- Integração de sistemas
- Design responsivo
- Experiência do usuário
- Documentação técnica

## 🚀 Possíveis Melhorias Futuras

- Sistema de pagamento real
- Upload de imagens de produtos
- Painel administrativo
- Busca e filtros avançados
- Sistema de avaliações
- Notificações por email
- Integração com APIs de frete
- Testes automatizados

---

**Desenvolvido para fins educacionais - Ensino Técnico**

