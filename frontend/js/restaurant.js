const BASE_URL = '';
const params = new URLSearchParams(window.location.search);
const restaurantId = params.get('id');
let cart = JSON.parse(localStorage.getItem('cart') || '[]');
let restaurantName = '';

async function loadRestaurant() {
    try {
        const [restaurant, menuData] = await Promise.all([
            fetch(`${BASE_URL}/api/restaurants/${restaurantId}`).then(r => r.json()),
            fetch(`${BASE_URL}/api/restaurants/${restaurantId}/menu`).then(r => r.json())
        ]);

        restaurantName = restaurant.name;
        document.title = `${restaurant.name} - Swiggy Clone`;

        document.getElementById('restaurant-header').innerHTML = `
            <img src="${restaurant.image}" alt="${restaurant.name}" onerror="this.src='https://placehold.co/120x100'">
            <div class="restaurant-header-info">
                <h1>${restaurant.name}</h1>
                <p class="cuisine">${restaurant.cuisine}</p>
                <div class="meta">
                    <span class="rating">⭐ ${restaurant.rating}</span>
                    <span>🕒 ${restaurant.delivery_time}</span>
                    <span>₹${restaurant.price_for_two} for two</span>
                </div>
            </div>
        `;

        const categories = Object.keys(menuData.categories);
        document.getElementById('category-sidebar').innerHTML = `
            <h3>Menu</h3>
            ${categories.map(cat => `
                <div class="category-item" onclick="scrollToCategory('${cat}', event)">${cat}</div>
            `).join('')}
        `;

        let menuHTML = '';
        categories.forEach(cat => {
            menuHTML += `<div class="menu-section" id="cat-${cat}">
                <h2>${cat}</h2>
                ${menuData.categories[cat].map(item => `
                    <div class="menu-item" id="item-${item.id}">
                        <img src="${item.image}" alt="${item.name}" onerror="this.src='https://placehold.co/100x90'">
                        <div class="menu-item-info">
                            <h3>${item.name}</h3>
                            <p>${item.description}</p>
                            <span class="item-price">₹${item.price}</span>
                        </div>
                        <div id="ctrl-${item.id}">${getItemControl(item)}</div>
                    </div>
                `).join('')}
            </div>`;
        });

        document.getElementById('menu-content').innerHTML = menuHTML;
        updateFloatingCart();
        updateCartBadge();
        loadReviews();
    } catch (e) {
        document.getElementById('menu-content').innerHTML = '<div class="loader">⚠️ Failed to load menu.</div>';
    }
}

async function loadReviews() {
    try {
        const reviews = await fetch(`${BASE_URL}/api/restaurants/${restaurantId}/reviews`).then(r => r.json());
        const section = document.getElementById('reviews-section');
        section.innerHTML = `
            <div style="background:var(--card-bg);border-radius:16px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:40px">
                <h2 style="font-size:18px;font-weight:700;margin-bottom:16px;color:var(--text)">⭐ Customer Reviews</h2>
                ${reviews.length === 0 ? '<p style="color:var(--gray)">No reviews yet. Be the first to review!</p>' :
                    reviews.map(r => `
                        <div style="padding:14px 0;border-bottom:1px solid var(--border)">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                                <span style="background:var(--green);color:white;padding:3px 8px;border-radius:6px;font-size:12px;font-weight:700">⭐ ${r.rating}</span>
                                <span style="font-weight:600;font-size:14px;color:var(--text)">${r.user_name}</span>
                                <span style="font-size:12px;color:var(--gray);margin-left:auto">${new Date(r.created_at).toLocaleDateString()}</span>
                            </div>
                            <p style="font-size:14px;color:var(--gray)">${r.comment}</p>
                        </div>
                    `).join('')
                }
            </div>
        `;
    } catch(e) {}
}

function getItemControl(item) {
    const existing = cart.find(c => c.id === item.id);
    const safeName = item.name.replace(/'/g, "\\'");
    if (existing) {
        return `<div class="qty-control">
            <button onclick="changeQty(${item.id}, -1, '${safeName}', ${item.price})">−</button>
            <span>${existing.quantity}</span>
            <button onclick="changeQty(${item.id}, 1, '${safeName}', ${item.price})">+</button>
        </div>`;
    }
    return `<button class="add-btn" onclick="addToCart(${item.id}, '${safeName}', ${item.price})">ADD</button>`;
}

function addToCart(id, name, price) {
    cart.push({ id, name, price, quantity: 1, restaurantId, restaurantName });
    saveCart();
    refreshItemControl(id, name, price);
    updateFloatingCart();
    updateCartBadge();
}

function changeQty(id, delta, name, price) {
    const idx = cart.findIndex(c => c.id === id);
    if (idx === -1) return;
    cart[idx].quantity += delta;
    if (cart[idx].quantity <= 0) cart.splice(idx, 1);
    saveCart();
    refreshItemControl(id, name, price);
    updateFloatingCart();
    updateCartBadge();
}

function refreshItemControl(id, name, price) {
    const ctrl = document.getElementById(`ctrl-${id}`);
    if (ctrl) ctrl.innerHTML = getItemControl({ id, name, price });
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function updateFloatingCart() {
    const fc = document.getElementById('floating-cart');
    const total = cart.reduce((sum, i) => sum + i.quantity, 0);
    const amount = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
    if (total > 0) {
        fc.classList.add('visible');
        fc.innerHTML = `<span>🛒 ${total} item${total > 1 ? 's' : ''}</span> <span>|</span> <span>View Cart ₹${amount}</span>`;
    } else {
        fc.classList.remove('visible');
    }
}

function scrollToCategory(cat, e) {
    document.getElementById(`cat-${cat}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    document.querySelectorAll('.category-item').forEach(c => c.classList.remove('active'));
    e.target.classList.add('active');
}

function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    const total = cart.reduce((sum, i) => sum + i.quantity, 0);
    badge.textContent = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
}

if (!restaurantId) window.location.href = '/';
else loadRestaurant();
