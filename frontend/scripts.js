// Configuração da API
const API_BASE = 'http://127.0.0.1:8000';

// Estado da aplicação
let appState = {
    products: [],
    cart: [],
    appliedCoupon: null,
    currentPage: 1,
    totalPages: 1,
    loading: false,
    searchTerm: '',
    sortBy: 'name',
    sortOrder: 'asc'
};

// Utilitários
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', { 
        style: 'currency', 
        currency: 'BRL' 
    }).format(value);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showAlert(message, type = 'error') {
    const container = document.getElementById('alertsContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: inherit; margin-left: auto; cursor: pointer;" aria-label="Fechar alerta">×</button>
    `;
    container.appendChild(alert);
    
    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

// API Client
const apiClient = {
    async call(endpoint, options = {}) {
        const token = localStorage.getItem('authToken');
        
        const defaultHeaders = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }
        
        const config = {
            headers: defaultHeaders,
            ...options
        };
        
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, config);
            
            if (response.status === 401) {
                localStorage.removeItem('authToken');
                updateAuthUI();
                return null;
            }
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Erro na API');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async getProducts(params = {}) {
        const queryParams = new URLSearchParams({
            page: params.page || 1,
            page_size: params.pageSize || 12,
            sort: params.sort || 'name',
            order: params.order || 'asc',
            ...params
        });
        
        return await this.call(`/products?${queryParams}`);
    },

    async validateCoupon(code) {
        return await this.call(`/coupons/${encodeURIComponent(code)}/validate`);
    },

    async confirmOrder(orderData) {
        return await this.call('/orders/confirm', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
    }
};

// Gerenciamento do carrinho
const cartManager = {
    getCart() {
        const saved = localStorage.getItem('cart');
        return saved ? JSON.parse(saved) : [];
    },

    saveCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
        appState.cart = cart;
        this.updateCartUI();
    },

    addItem(product, quantity = 1) {
        const cart = this.getCart();
        const existingItem = cart.find(item => item.product_id === product.id);
        
        if (existingItem) {
            existingItem.quantity += quantity;
            // Verificar limite de estoque
            if (existingItem.quantity > product.stock) {
                existingItem.quantity = product.stock;
                showAlert(`Quantidade limitada ao estoque disponível (${product.stock})`, 'warning');
            }
        } else {
            cart.push({
                product_id: product.id,
                quantity: Math.min(quantity, product.stock),
                product: product
            });
        }
        
        this.saveCart(cart);
        showAlert(`${product.name} adicionado ao carrinho!`, 'success');
    },

    updateQuantity(productId, quantity) {
        const cart = this.getCart();
        const item = cart.find(item => item.product_id === productId);
        
        if (!item) return;
        
        if (quantity <= 0) {
            this.removeItem(productId);
            return;
        }
        
        // Verificar limite de estoque
        if (quantity > item.product.stock) {
            quantity = item.product.stock;
            showAlert(`Quantidade limitada ao estoque disponível (${item.product.stock})`, 'warning');
        }
        
        item.quantity = quantity;
        this.saveCart(cart);
    },

    removeItem(productId) {
        const cart = this.getCart();
        const updatedCart = cart.filter(item => item.product_id !== productId);
        this.saveCart(updatedCart);
        showAlert('Item removido do carrinho', 'success');
    },

    clear() {
        this.saveCart([]);
        this.clearAppliedCoupon();
    },

    getTotal() {
        const cart = this.getCart();
        return cart.reduce((total, item) => {
            const price = parseFloat(item.product.price);
            return total + (price * item.quantity);
        }, 0);
    },

    getAppliedCoupon() {
        const saved = localStorage.getItem('appliedCoupon');
        return saved ? JSON.parse(saved) : null;
    },

    saveAppliedCoupon(coupon) {
        localStorage.setItem('appliedCoupon', JSON.stringify(coupon));
        appState.appliedCoupon = coupon;
        this.updateCartUI();
    },

    clearAppliedCoupon() {
        localStorage.removeItem('appliedCoupon');
        appState.appliedCoupon = null;
        this.updateCartUI();
    },

    getTotalWithDiscount() {
        const subtotal = this.getTotal();
        const coupon = this.getAppliedCoupon();
        
        if (!coupon || !coupon.valid) {
            return { subtotal, discount: 0, total: subtotal };
        }
        
        const discount = subtotal * (coupon.discount_percent / 100);
        const total = subtotal - discount;
        
        return { subtotal, discount, total };
    },

    updateCartUI() {
        const cart = this.getCart();
        const badge = document.getElementById('cartBadge');
        const cartItems = document.getElementById('cartItems');
        const cartEmpty = document.getElementById('cartEmpty');
        const cartFooter = document.getElementById('cartFooter');
        
        // Atualizar badge
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = totalItems;
        badge.style.display = totalItems > 0 ? 'flex' : 'none';
        
        // Atualizar conteúdo do carrinho
        if (cart.length === 0) {
            cartEmpty.style.display = 'block';
            cartItems.style.display = 'none';
            cartFooter.style.display = 'none';
        } else {
            cartEmpty.style.display = 'none';
            cartItems.style.display = 'block';
            cartFooter.style.display = 'block';
            
            cartItems.innerHTML = cart.map(item => `
                <div class="cart-item">
                    <img 
                        src="${item.product.image_url || '/assets/placeholder.png'}" 
                        alt="${item.product.name}"
                        class="cart-item-image"
                        onerror="this.src='/assets/placeholder.png'"
                        loading="lazy"
                    >
                    <div class="cart-item-info">
                        <div class="cart-item-name">${item.product.name}</div>
                        <div class="cart-item-price">${formatCurrency(parseFloat(item.product.price))}</div>
                        <div class="cart-item-controls">
                            <button 
                                class="btn-quantity" 
                                onclick="cartManager.updateQuantity(${item.product_id}, ${item.quantity - 1})"
                                ${item.quantity <= 1 ? 'disabled' : ''}
                                aria-label="Diminuir quantidade"
                            >-</button>
                            <span class="quantity-display">${item.quantity}</span>
                            <button 
                                class="btn-quantity" 
                                onclick="cartManager.updateQuantity(${item.product_id}, ${item.quantity + 1})"
                                ${item.quantity >= item.product.stock ? 'disabled' : ''}
                                aria-label="Aumentar quantidade"
                            >+</button>
                            <button 
                                class="btn-remove" 
                                onclick="cartManager.removeItem(${item.product_id})"
                                aria-label="Remover item"
                            >Remover</button>
                        </div>
                    </div>
                </div>
            `).join('');
            
            // Atualizar totais
            this.updateTotals();
        }
    },

    updateTotals() {
        const { subtotal, discount, total } = this.getTotalWithDiscount();
        
        document.getElementById('cartSubtotal').textContent = formatCurrency(subtotal);
        document.getElementById('cartTotal').textContent = formatCurrency(total);
        
        const discountLine = document.getElementById('discountLine');
        const cartDiscount = document.getElementById('cartDiscount');
        
        if (discount > 0) {
            discountLine.style.display = 'flex';
            cartDiscount.textContent = `- ${formatCurrency(discount)}`;
        } else {
            discountLine.style.display = 'none';
        }
        
        // Atualizar botão de checkout
        const checkoutBtn = document.getElementById('checkoutBtn');
        checkoutBtn.disabled = this.getCart().length === 0;
    }
};

// Gerenciamento de cupons
const couponManager = {
    async applyCoupon(code) {
        if (!code || code.trim() === '') {
            showAlert('Digite um código de cupom válido', 'error');
            return;
        }
        
        try {
            const response = await apiClient.validateCoupon(code.trim());
            
            if (response.valid) {
                cartManager.saveAppliedCoupon(response);
                this.updateCouponUI(response);
                showAlert(`Cupom ${response.code} aplicado com sucesso!`, 'success');
            } else {
                showAlert(response.message || 'Cupom inválido', 'error');
            }
        } catch (error) {
            console.error('Erro ao validar cupom:', error);
            showAlert('Erro ao validar cupom', 'error');
        }
    },

    removeCoupon() {
        cartManager.clearAppliedCoupon();
        this.updateCouponUI(null);
        showAlert('Cupom removido', 'success');
    },

    updateCouponUI(coupon) {
        const inputGroup = document.getElementById('couponInputGroup');
        const appliedDiv = document.getElementById('couponApplied');
        const appliedText = document.getElementById('couponAppliedText');
        
        if (coupon && coupon.valid) {
            inputGroup.style.display = 'none';
            appliedDiv.style.display = 'flex';
            appliedText.textContent = `Cupom ${coupon.code} aplicado (${coupon.discount_percent}% off)`;
        } else {
            inputGroup.style.display = 'flex';
            appliedDiv.style.display = 'none';
            document.getElementById('couponInput').value = '';
        }
    }
};

// Gerenciamento de produtos
const productManager = {
    async loadProducts(params = {}) {
        const loadingState = document.getElementById('loadingState');
        const emptyState = document.getElementById('emptyState');
        const productsGrid = document.getElementById('productsGrid');
        
        loadingState.style.display = 'block';
        emptyState.style.display = 'none';
        productsGrid.innerHTML = '';
        
        try {
            const response = await apiClient.getProducts({
                search: appState.searchTerm,
                sort: appState.sortBy,
                order: appState.sortOrder,
                page: appState.currentPage,
                page_size: 12,
                ...params
            });
            
            if (response && response.data) {
                appState.products = response.data;
                this.renderProducts(response.data);
                
                if (response.data.length === 0) {
                    emptyState.style.display = 'block';
                }
            }
        } catch (error) {
            console.error('Erro ao carregar produtos:', error);
            showAlert('Erro ao carregar produtos', 'error');
            emptyState.style.display = 'block';
        } finally {
            loadingState.style.display = 'none';
        }
    },

    renderProducts(products) {
        const grid = document.getElementById('productsGrid');
        
        grid.innerHTML = products.map(product => `
            <article class="product-card">
                <img 
                    src="${product.image_url || '/assets/placeholder.png'}" 
                    alt="${product.name}"
                    class="product-image"
                    onerror="this.src='/assets/placeholder.png'"
                    loading="lazy"
                >
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    ${product.description ? `<p class="product-description">${product.description}</p>` : ''}
                    <p class="product-stock">Estoque: ${product.stock} unidades</p>
                    <div class="product-footer">
                        <span class="product-price">${formatCurrency(parseFloat(product.price))}</span>
                        <button 
                            class="btn-add-cart" 
                            onclick="cartManager.addItem(${JSON.stringify(product).replace(/"/g, '&quot;')}, 1)"
                            ${product.stock === 0 ? 'disabled title="Produto fora de estoque"' : ''}
                            aria-label="Adicionar ${product.name} ao carrinho"
                        >
                            ${product.stock === 0 ? 'Fora de Estoque' : '🛒 Adicionar'}
                        </button>
                    </div>
                </div>
            </article>
        `).join('');
    },

    applyFilters() {
        const searchInput = document.getElementById('searchInput');
        const sortSelect = document.getElementById('sortSelect');
        const orderSelect = document.getElementById('orderSelect');
        
        appState.searchTerm = searchInput.value.trim();
        appState.sortBy = sortSelect.value;
        appState.sortOrder = orderSelect.value;
        appState.currentPage = 1;
        
        this.loadProducts();
    }
};

// Gerenciamento de autenticação
function updateAuthUI() {
    const token = localStorage.getItem('authToken');
    const authButtons = document.getElementById('authButtons');
    const userMenu = document.getElementById('userMenu');
    
    if (token) {
        if (authButtons) authButtons.style.display = 'none';
        if (userMenu) userMenu.style.display = 'flex';
    } else {
        if (authButtons) authButtons.style.display = 'flex';
        if (userMenu) userMenu.style.display = 'none';
    }
}

// Gerenciamento do modal do carrinho
const cartModal = {
    open() {
        const overlay = document.getElementById('cartOverlay');
        overlay.classList.add('active');
        overlay.setAttribute('aria-hidden', 'false');
        
        // Focar no botão de fechar para acessibilidade
        setTimeout(() => {
            document.getElementById('closeCartBtn').focus();
        }, 100);
        
        // Desabilitar scroll do body
        document.body.style.overflow = 'hidden';
    },

    close() {
        const overlay = document.getElementById('cartOverlay');
        overlay.classList.remove('active');
        overlay.setAttribute('aria-hidden', 'true');
        
        // Reabilitar scroll do body
        document.body.style.overflow = '';
        
        // Retornar foco para o botão do carrinho
        document.getElementById('cartButton').focus();
    }
};

// Gerenciamento de pedidos
const orderManager = {
    async confirmOrder() {
        const cart = cartManager.getCart();
        if (cart.length === 0) {
            showAlert('Carrinho vazio', 'error');
            return;
        }
        
        const checkoutBtn = document.getElementById('checkoutBtn');
        const originalText = checkoutBtn.innerHTML;
        
        try {
            checkoutBtn.disabled = true;
            checkoutBtn.innerHTML = '<span class="spinner"></span> Processando...';
            
            const orderData = {
                items: cart.map(item => ({
                    product_id: item.product_id,
                    quantity: item.quantity
                })),
                coupon_code: appState.appliedCoupon ? appState.appliedCoupon.code : undefined
            };
            
            const order = await apiClient.confirmOrder(orderData);
            
            if (order) {
                // Limpar carrinho
                cartManager.clear();
                cartModal.close();
                
                // Mostrar sucesso
                showAlert(`Pedido #${order.id} confirmado com sucesso! Total: ${formatCurrency(parseFloat(order.total_final))}`, 'success');
                
                // Recarregar produtos para atualizar estoque
                productManager.loadProducts();
            }
            
        } catch (error) {
            console.error('Erro ao confirmar pedido:', error);
            showAlert('Erro ao confirmar pedido: ' + error.message, 'error');
        } finally {
            checkoutBtn.disabled = false;
            checkoutBtn.innerHTML = originalText;
        }
    }
};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar estado
    appState.cart = cartManager.getCart();
    appState.appliedCoupon = cartManager.getAppliedCoupon();
    
    // Atualizar UI inicial
    updateAuthUI();
    cartManager.updateCartUI();
    couponManager.updateCouponUI(appState.appliedCoupon);
    
    // Carregar produtos
    productManager.loadProducts();
    
    // Event listeners - Busca com debounce
    const searchInput = document.getElementById('searchInput');
    const debouncedSearch = debounce(() => {
        productManager.applyFilters();
    }, 300);
    
    searchInput.addEventListener('input', debouncedSearch);
    
    // Event listeners - Filtros
    document.getElementById('sortSelect').addEventListener('change', () => {
        productManager.applyFilters();
    });
    
    document.getElementById('orderSelect').addEventListener('change', () => {
        productManager.applyFilters();
    });
    
    // Event listeners - Carrinho
    document.getElementById('cartButton').addEventListener('click', () => {
        cartModal.open();
    });
    
    document.getElementById('closeCartBtn').addEventListener('click', () => {
        cartModal.close();
    });
    
    // Fechar carrinho com ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const overlay = document.getElementById('cartOverlay');
            if (overlay.classList.contains('active')) {
                cartModal.close();
            }
        }
    });
    
    // Fechar carrinho clicando no overlay
    document.getElementById('cartOverlay').addEventListener('click', (e) => {
        if (e.target.id === 'cartOverlay') {
            cartModal.close();
        }
    });
    
    // Event listeners - Cupom
    document.getElementById('applyCouponBtn').addEventListener('click', () => {
        const code = document.getElementById('couponInput').value;
        couponManager.applyCoupon(code);
    });
    
    document.getElementById('couponInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const code = e.target.value;
            couponManager.applyCoupon(code);
        }
    });
    
    document.getElementById('removeCouponBtn').addEventListener('click', () => {
        couponManager.removeCoupon();
    });
    
    // Event listeners - Checkout
    document.getElementById('checkoutBtn').addEventListener('click', () => {
        orderManager.confirmOrder();
    });
    
    // Event listeners - Logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('authToken');
            updateAuthUI();
            showAlert('Logout realizado com sucesso!', 'success');
        });
    }
});

// Funções globais para uso inline
window.cartManager = cartManager;
window.couponManager = couponManager;
window.orderManager = orderManager;