const BASE_URL = '';
let allRestaurants = [];

const auth = {
    getUser: () => JSON.parse(localStorage.getItem('user') || 'null'),
    logout: () => { localStorage.removeItem('user'); window.location.href = '/'; }
};

async function loadRestaurants(search = '') {
    const grid = document.getElementById('restaurants-grid');
    grid.innerHTML = Array(6).fill(`
        <div class="skeleton-card">
            <div class="skeleton skeleton-img"></div>
            <div class="skeleton skeleton-line medium"></div>
            <div class="skeleton skeleton-line short"></div>
        </div>
    `).join('');
    try {
        const res = await fetch(`${BASE_URL}/api/restaurants?search=${encodeURIComponent(search)}`);
        allRestaurants = await res.json();
        renderRestaurants(allRestaurants);
    } catch {
        grid.innerHTML = `
            <div class="no-results">
                ⚠️ Could not connect to server.<br>
                <small style="font-size:13px;margin-top:8px;display:block">Make sure backend is running: <b>python app.py</b></small>
                <button class="btn-primary" style="margin-top:16px" onclick="loadRestaurants()">Retry</button>
            </div>`;
    }
}

function renderRestaurants(restaurants) {
    const grid = document.getElementById('restaurants-grid');
    if (!restaurants.length) {
        grid.innerHTML = '<div class="no-results">😕 No restaurants found.</div>';
        return;
    }
    const badges = ['', '🔥 Trending', '⚡ Fast', '🌟 Popular', '', '💚 Healthy', '', '🆕 New', '', '🔥 Trending'];
    grid.innerHTML = restaurants.map((r, i) => `
        <div class="restaurant-card" onclick="window.location.href='/restaurant.html?id=${r.id}'">
            <div class="card-img-wrap">
                <img src="${r.image}" alt="${r.name}" onerror="this.src='https://placehold.co/400x180?text=${encodeURIComponent(r.name)}'">
                ${badges[i % badges.length] ? `<span class="card-badge">${badges[i % badges.length]}</span>` : ''}
            </div>
            <div class="card-info">
                <h3>${r.name}</h3>
                <p class="cuisine">${r.cuisine}</p>
                <div class="card-meta">
                    <span class="rating">⭐ ${r.rating}</span>
                    <span class="delivery-time">${r.delivery_time}</span>
                    <span class="price">₹${r.price_for_two} for two</span>
                </div>
            </div>
        </div>
    `).join('');
}

function filterByChip(cuisine, el) {
    document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    if (cuisine === 'all') return renderRestaurants(allRestaurants);
    const filtered = allRestaurants.filter(r => r.cuisine.toLowerCase().includes(cuisine.toLowerCase()));
    renderRestaurants(filtered);
}

function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const badge = document.getElementById('cart-badge');
    const total = cart.reduce((sum, i) => sum + i.quantity, 0);
    badge.textContent = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
    badge.classList.remove('pop');
    void badge.offsetWidth;
    badge.classList.add('pop');
}

let searchTimer;
document.getElementById('search-input').addEventListener('input', (e) => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
        const val = e.target.value.trim();
        if (val === '') renderRestaurants(allRestaurants);
        else {
            const filtered = allRestaurants.filter(r =>
                r.name.toLowerCase().includes(val.toLowerCase()) ||
                r.cuisine.toLowerCase().includes(val.toLowerCase())
            );
            renderRestaurants(filtered);
        }
    }, 300);
});

document.getElementById('search-input').addEventListener('keyup', (e) => {
    if (e.key === 'Enter') loadRestaurants(e.target.value);
});

document.getElementById('search-btn').addEventListener('click', () => {
    loadRestaurants(document.getElementById('search-input').value);
});

updateCartBadge();
loadRestaurants();
