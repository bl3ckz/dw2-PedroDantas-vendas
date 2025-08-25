## Esquema do Banco de Dados

### Tabela: `users`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `name` (TEXT NOT NULL)
- `email` (TEXT NOT NULL UNIQUE)
- `password` (TEXT NOT NULL)

### Tabela: `products`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `name` (TEXT NOT NULL)
- `description` (TEXT)
- `price` (REAL NOT NULL)
- `image` (TEXT)

### Tabela: `orders`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))
- `date` (TEXT NOT NULL) -- Formato YYYY-MM-DD HH:MM:SS
- `status` (TEXT NOT NULL) -- Ex: 'pending', 'completed', 'cancelled'

### Tabela: `order_items`
- `order_id` (INTEGER NOT NULL, FOREIGN KEY (order_id) REFERENCES orders(id))
- `product_id` (INTEGER NOT NULL, FOREIGN KEY (product_id) REFERENCES products(id))
- `quantity` (INTEGER NOT NULL)
- PRIMARY KEY (`order_id`, `product_id`)


