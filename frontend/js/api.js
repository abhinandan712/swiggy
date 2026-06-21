const BASE_URL = '';

const api = {
    getRestaurants: (search = '') =>
        fetch(`${BASE_URL}/api/restaurants?search=${search}`).then(r => r.json()),

    getRestaurant: (id) =>
        fetch(`${BASE_URL}/api/restaurants/${id}`).then(r => r.json()),

    getMenu: (restaurantId) =>
        fetch(`${BASE_URL}/api/restaurants/${restaurantId}/menu`).then(r => r.json()),

    placeOrder: (orderData) =>
        fetch(`${BASE_URL}/api/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        }).then(r => r.json()),

    getOrder: (orderId) =>
        fetch(`${BASE_URL}/api/orders/${orderId}`).then(r => r.json()),

    trackOrder: (orderId) =>
        fetch(`${BASE_URL}/api/orders/${orderId}/track`).then(r => r.json()),

    startTracking: (orderId) =>
        fetch(`${BASE_URL}/api/orders/${orderId}/start-tracking`, { method: 'POST' }).then(r => r.json()),

    getReviews: (restaurantId) =>
        fetch(`${BASE_URL}/api/restaurants/${restaurantId}/reviews`).then(r => r.json()),

    addReview: (restaurantId, data) =>
        fetch(`${BASE_URL}/api/restaurants/${restaurantId}/reviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json()),

    signup: (data) =>
        fetch(`${BASE_URL}/api/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json()),

    login: (data) =>
        fetch(`${BASE_URL}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json()),
};

// Auth helpers
const auth = {
    getUser: () => JSON.parse(localStorage.getItem('user') || 'null'),
    setUser: (user) => localStorage.setItem('user', JSON.stringify(user)),
    logout: () => { localStorage.removeItem('user'); window.location.href = 'index.html'; },
    isLoggedIn: () => !!localStorage.getItem('user')
};
