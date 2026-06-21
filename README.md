# 🍔 Swiggy Clone

A full stack food delivery app built with HTML/CSS/JS (frontend) and Python Flask (backend).

## Features
- 🏠 Restaurant listing with search & filter
- 🍕 Restaurant menu with categories
- 🛒 Add to cart / update quantities
- 📦 Place orders with delivery details
- ✅ Order confirmation page

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **Database:** SQLite

## Setup & Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Server runs at: http://localhost:5000

### Frontend
Open `frontend/index.html` directly in your browser.
> Or use Live Server extension in VS Code for best experience.

## Project Structure
```
swiggy-clone/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── routes/
│   │   ├── restaurants.py
│   │   ├── menu.py
│   │   └── orders.py
│   └── requirements.txt
└── frontend/
    ├── index.html        ← Home (restaurant listing)
    ├── restaurant.html   ← Menu page
    ├── cart.html         ← Cart & checkout
    ├── order.html        ← Order confirmation
    ├── css/
    └── js/
```
