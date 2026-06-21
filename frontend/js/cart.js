const BASE_URL = '';
let cart = JSON.parse(localStorage.getItem('cart') || '[]');
let selectedMethod = 'card';
let discount = 0;

const PROMO_CODES = {
    'FIRST50':   { type: 'percent', value: 50, max: 150, label: '50% off applied!' },
    'FREEDEL':   { type: 'flat',    value: 0,  max: 0,   label: 'Free delivery applied!' },
    'PIZZA2X':   { type: 'percent', value: 20, max: 100, label: '20% off applied!' },
    'BIRYANI100':{ type: 'flat',    value: 100,max: 100, label: '₹100 off applied!' },
    'NIGHT20':   { type: 'percent', value: 20, max: 80,  label: '20% off applied!' },
    'WELCOME30': { type: 'percent', value: 30, max: 120, label: '30% off applied!' },
};

function getTotal() {
    const subtotal = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
    return Math.max(0, subtotal - discount);
}

function renderCart() {
    const section = document.getElementById('cart-items');
    const badge = document.getElementById('cart-badge');
    const totalItems = cart.reduce((sum, i) => sum + i.quantity, 0);
    badge.textContent = totalItems;
    badge.style.display = totalItems > 0 ? 'flex' : 'none';

    if (!cart.length) {
        section.innerHTML = `
            <div class="empty-cart">
                <div class="icon">🛒</div>
                <h3>Your cart is empty</h3>
                <p>Add items from a restaurant to get started</p>
                <button class="btn-primary" onclick="window.location.href='/'">Browse Restaurants</button>
            </div>`;
        document.getElementById('order-summary').style.display = 'none';
        return;
    }

    document.getElementById('order-summary').style.display = 'block';
    section.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <p class="item-price">₹${item.price} each</p>
            </div>
            <div class="cart-qty-control">
                <button onclick="changeQty(${item.id}, -1)">−</button>
                <span>${item.quantity}</span>
                <button onclick="changeQty(${item.id}, 1)">+</button>
            </div>
            <div class="item-total">₹${item.price * item.quantity}</div>
        </div>
    `).join('');
    updateSummary();
}

function changeQty(id, delta) {
    const idx = cart.findIndex(i => i.id === id);
    if (idx === -1) return;
    cart[idx].quantity += delta;
    if (cart[idx].quantity <= 0) cart.splice(idx, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCart();
}

function updateSummary() {
    document.getElementById('total').textContent = `₹${getTotal()}`;
}

// Payment modal
function openPayment() {
    const name = document.getElementById('customer-name').value.trim();
    const address = document.getElementById('address').value.trim();
    if (!name || !address) return alert('Please fill in your name and address.');
    document.getElementById('modal-amount').textContent = `₹${getTotal()}`;
    document.getElementById('payment-modal').classList.add('open');
}

function closePayment() {
    document.getElementById('payment-modal').classList.remove('open');
    resetModal();
}

function resetModal() {
    document.getElementById('payment-form-section').style.display = 'block';
    document.getElementById('processing-section').classList.remove('show');
    document.getElementById('success-section').classList.remove('show');
}

function selectMethod(method, el) {
    selectedMethod = method;
    document.querySelectorAll('.pay-method').forEach(m => m.classList.remove('active'));
    el.classList.add('active');
    document.querySelectorAll('.pay-form').forEach(f => f.classList.remove('active'));
    document.getElementById(`form-${method}`).classList.add('active');
    const btn = document.getElementById('pay-btn');
    btn.textContent = method === 'cod' ? 'Confirm Order 🎉' : 'Pay Now 🔒';
}

function selectUPI(el) {
    document.querySelectorAll('.upi-app').forEach(u => u.classList.remove('selected'));
    el.classList.add('selected');
}

function formatCard(input) {
    let val = input.value.replace(/\D/g, '').substring(0, 16);
    input.value = val.replace(/(.{4})/g, '$1 ').trim();
    const display = val.padEnd(16, '•').replace(/(.{4})/g, '$1 ').trim();
    document.getElementById('preview-number').textContent = display;
}

function formatExpiry(input) {
    let val = input.value.replace(/\D/g, '').substring(0, 4);
    if (val.length >= 2) val = val.substring(0,2) + '/' + val.substring(2);
    input.value = val;
    document.getElementById('preview-expiry').textContent = val || 'MM/YY';
}

function applyPromo() {
    const code = document.getElementById('promo-input').value.trim().toUpperCase();
    const msgEl = document.getElementById('promo-msg');
    const promo = PROMO_CODES[code];

    if (!promo) {
        msgEl.textContent = '❌ Invalid promo code.';
        msgEl.className = 'promo-msg error';
        discount = 0;
    } else {
        const subtotal = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
        if (promo.type === 'percent') {
            discount = Math.min(Math.round(subtotal * promo.value / 100), promo.max);
        } else {
            discount = promo.value;
        }
        msgEl.textContent = `✅ ${promo.label} (−₹${discount})`;
        msgEl.className = 'promo-msg success';
    }
    updateSummary();
    document.getElementById('modal-amount').textContent = `₹${getTotal()}`;
}

function validatePayment() {
    if (selectedMethod === 'card') {
        const num = document.getElementById('card-number').value.replace(/\s/g, '');
        const name = document.getElementById('card-name').value.trim();
        const expiry = document.getElementById('card-expiry').value.trim();
        const cvv = document.getElementById('card-cvv').value.trim();
        if (num.length < 16) return 'Please enter a valid 16-digit card number.';
        if (!name) return 'Please enter cardholder name.';
        if (expiry.length < 5) return 'Please enter a valid expiry date.';
        if (cvv.length < 3) return 'Please enter a valid CVV.';
    } else if (selectedMethod === 'upi') {
        const upiId = document.getElementById('upi-id').value.trim();
        if (!upiId.includes('@')) return 'Please enter a valid UPI ID (e.g. name@upi).';
    } else if (selectedMethod === 'netbanking') {
        if (!document.getElementById('bank-select').value) return 'Please select a bank.';
    }
    return null;
}

async function processPayment() {
    const error = validatePayment();
    if (error) return alert(error);

    const formSection = document.getElementById('payment-form-section');
    const processing = document.getElementById('processing-section');
    const success = document.getElementById('success-section');
    const processingText = document.getElementById('processing-text');

    // Show processing
    formSection.style.display = 'none';
    processing.classList.add('show');

    const steps = [
        { text: 'Connecting to payment gateway...', delay: 800 },
        { text: 'Verifying payment details...', delay: 900 },
        { text: 'Authorizing transaction...', delay: 900 },
        { text: 'Payment successful! 🎉', delay: 600 },
    ];

    for (const step of steps) {
        processingText.textContent = step.text;
        await new Promise(r => setTimeout(r, step.delay));
    }

    // Show success
    processing.classList.remove('show');
    success.classList.add('show');

    // Place order in backend
    await new Promise(r => setTimeout(r, 1000));
    try {
        const name = document.getElementById('customer-name').value.trim();
        const address = document.getElementById('address').value.trim();
        const result = await fetch(`${BASE_URL}/api/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                customer_name: name,
                address,
                items: cart.map(i => ({ name: i.name, price: i.price, quantity: i.quantity }))
            })
        }).then(r => r.json());

        localStorage.removeItem('cart');
        window.location.href = `/order.html?id=${result.order_id}`;
    } catch {
        alert('Payment done but order failed. Please try again.');
        closePayment();
    }
}

// Close modal on overlay click
document.getElementById('payment-modal').addEventListener('click', function(e) {
    if (e.target === this) closePayment();
});

renderCart();
