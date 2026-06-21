import sqlite3

DB_NAME = "swiggy.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cuisine TEXT,
            rating REAL,
            delivery_time TEXT,
            price_for_two INTEGER,
            image TEXT,
            location TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            name TEXT NOT NULL,
            category TEXT,
            price INTEGER,
            description TEXT,
            image TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            address TEXT,
            total INTEGER,
            status TEXT DEFAULT 'Placed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_name TEXT,
            quantity INTEGER,
            price INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')

    # Seed restaurants
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    if cursor.fetchone()[0] == 0:
        restaurants = [
            ("Burger King", "Burgers, Fast Food", 4.2, "30-40 mins", 400, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400", "Mumbai"),
            ("Pizza Hut", "Pizza, Italian", 4.0, "40-50 mins", 600, "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400", "Delhi"),
            ("Domino's", "Pizza, Fast Food", 4.3, "25-35 mins", 500, "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400", "Bangalore"),
            ("KFC", "Chicken, Fast Food", 4.1, "30-40 mins", 450, "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=400", "Chennai"),
            ("Subway", "Sandwiches, Healthy", 3.9, "20-30 mins", 350, "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=400", "Hyderabad"),
            ("McDonald's", "Burgers, Fast Food", 4.4, "20-30 mins", 400, "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=400", "Pune"),
            ("Biryani Blues", "Biryani, North Indian", 4.5, "35-45 mins", 500, "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400", "Mumbai"),
            ("Haldiram's", "Snacks, Indian, Sweets", 4.3, "20-30 mins", 300, "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400", "Delhi"),
            ("Behrouz Biryani", "Biryani, Mughlai", 4.6, "40-50 mins", 700, "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400", "Bangalore"),
            ("Wow! Momo", "Momos, Chinese, Tibetan", 4.2, "25-35 mins", 300, "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400", "Kolkata"),
            ("Faasos", "Wraps, Rolls, Fast Food", 4.0, "30-40 mins", 350, "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400", "Mumbai"),
            ("Barbeque Nation", "BBQ, North Indian, Kebabs", 4.7, "45-55 mins", 1200, "https://images.unsplash.com/photo-1544025162-d76694265947?w=400", "Delhi"),
            ("Box8", "Indian, Home Style", 4.1, "30-40 mins", 400, "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400", "Pune"),
            ("Taco Bell", "Mexican, Fast Food", 4.0, "25-35 mins", 450, "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400", "Bangalore"),
            ("Paradise Biryani", "Biryani, Hyderabadi", 4.8, "40-50 mins", 600, "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400", "Hyderabad"),
            ("Rolls Mania", "Rolls, Wraps, Street Food", 3.9, "20-30 mins", 250, "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400", "Mumbai"),
            ("Sushi Garden", "Japanese, Sushi", 4.4, "45-55 mins", 1000, "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400", "Bangalore"),
            ("The Belgian Waffle", "Waffles, Desserts, Cafe", 4.3, "20-30 mins", 400, "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=400", "Delhi"),
            ("Punjabi Tadka", "North Indian, Punjabi", 4.2, "35-45 mins", 500, "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400", "Amritsar"),
            ("Noodle House", "Chinese, Noodles, Asian", 4.1, "30-40 mins", 400, "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400", "Mumbai"),
        ]
        cursor.executemany("INSERT INTO restaurants (name, cuisine, rating, delivery_time, price_for_two, image, location) VALUES (?,?,?,?,?,?,?)", restaurants)

    # Seed menu items
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        menu_items = [
            # Burger King
            (1, "Whopper", "Burgers", 199, "Flame-grilled beef patty", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300"),
            (1, "Chicken Burger", "Burgers", 149, "Crispy chicken patty", "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=300"),
            (1, "French Fries", "Sides", 99, "Crispy golden fries", "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300"),
            (1, "Cold Drink", "Beverages", 59, "Chilled soft drink", "https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=300"),
            # Pizza Hut
            (2, "Margherita Pizza", "Pizza", 299, "Classic tomato & cheese", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"),
            (2, "Pepperoni Pizza", "Pizza", 399, "Loaded with pepperoni", "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300"),
            (2, "Garlic Bread", "Sides", 149, "Toasted with garlic butter", "https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?w=300"),
            # Domino's
            (3, "Farmhouse Pizza", "Pizza", 349, "Loaded veggies pizza", "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300"),
            (3, "Pasta", "Pasta", 249, "Creamy white sauce pasta", "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=300"),
            # KFC
            (4, "Zinger Burger", "Burgers", 179, "Spicy crispy chicken", "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=300"),
            (4, "Popcorn Chicken", "Snacks", 149, "Bite-sized crispy chicken", "https://images.unsplash.com/photo-1562967914-608f82629710?w=300"),
            # Subway
            (5, "Veggie Delight", "Sandwiches", 199, "Fresh veggies sub", "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=300"),
            (5, "Chicken Teriyaki", "Sandwiches", 249, "Grilled chicken sub", "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=300"),
            # McDonald's
            (6, "McAloo Tikki", "Burgers", 99, "Spiced potato patty", "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=300"),
            (6, "McSpicy Chicken", "Burgers", 169, "Spicy chicken burger", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300"),
            (6, "McFlurry", "Desserts", 129, "Creamy ice cream", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300"),
            # Biryani Blues
            (7, "Chicken Biryani", "Biryani", 299, "Aromatic basmati rice with chicken", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300"),
            (7, "Mutton Biryani", "Biryani", 399, "Slow cooked mutton biryani", "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=300"),
            (7, "Veg Biryani", "Biryani", 249, "Fresh vegetable biryani", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300"),
            (7, "Raita", "Sides", 59, "Cool yogurt with spices", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            # Haldiram's
            (8, "Samosa", "Snacks", 49, "Crispy fried samosa", "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300"),
            (8, "Chole Bhature", "Main Course", 149, "Spicy chickpea with fried bread", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            (8, "Gulab Jamun", "Sweets", 79, "Soft syrup soaked dumplings", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300"),
            (8, "Lassi", "Beverages", 89, "Chilled sweet yogurt drink", "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300"),
            # Behrouz Biryani
            (9, "Royal Chicken Biryani", "Biryani", 449, "Premium slow cooked biryani", "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=300"),
            (9, "Shahi Mutton Biryani", "Biryani", 549, "Rich mughlai mutton biryani", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300"),
            (9, "Seekh Kebab", "Starters", 299, "Minced meat kebabs on skewer", "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"),
            # Wow! Momo
            (10, "Steamed Momos", "Momos", 129, "Soft steamed dumplings", "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"),
            (10, "Fried Momos", "Momos", 149, "Crispy fried dumplings", "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"),
            (10, "Momo Soup", "Soups", 99, "Hot spicy momo soup", "https://images.unsplash.com/photo-1547592180-85f173990554?w=300"),
            (10, "Tandoori Momos", "Momos", 169, "Grilled tandoori momos", "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"),
            # Faasos
            (11, "Chicken Tikka Wrap", "Wraps", 199, "Spicy chicken tikka wrap", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            (11, "Paneer Wrap", "Wraps", 179, "Grilled paneer wrap", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            (11, "Egg Roll", "Rolls", 149, "Classic egg roll", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            # Barbeque Nation
            (12, "BBQ Chicken", "BBQ", 499, "Grilled BBQ chicken", "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"),
            (12, "Mutton Seekh", "Kebabs", 449, "Juicy mutton seekh kebab", "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"),
            (12, "Paneer Tikka", "Starters", 349, "Grilled cottage cheese tikka", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            (12, "Dal Makhani", "Main Course", 299, "Creamy black lentil curry", "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300"),
            # Box8
            (13, "Dal Rice", "Meals", 149, "Homestyle dal with steamed rice", "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300"),
            (13, "Butter Chicken", "Main Course", 249, "Creamy tomato butter chicken", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            (13, "Paneer Butter Masala", "Main Course", 229, "Rich paneer in butter gravy", "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300"),
            # Taco Bell
            (14, "Crunchy Taco", "Tacos", 149, "Classic crunchy beef taco", "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=300"),
            (14, "Burrito", "Burritos", 249, "Loaded chicken burrito", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            (14, "Nachos", "Snacks", 179, "Cheesy nachos with salsa", "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=300"),
            (14, "Quesadilla", "Snacks", 199, "Grilled cheese quesadilla", "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=300"),
            # Paradise Biryani
            (15, "Hyderabadi Dum Biryani", "Biryani", 349, "Authentic dum cooked biryani", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300"),
            (15, "Mirchi Ka Salan", "Sides", 99, "Spicy chilli curry", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            (15, "Double Ka Meetha", "Desserts", 129, "Hyderabadi bread pudding", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300"),
            # Rolls Mania
            (16, "Chicken Roll", "Rolls", 129, "Spicy chicken kathi roll", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            (16, "Paneer Roll", "Rolls", 119, "Grilled paneer kathi roll", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            (16, "Egg Roll", "Rolls", 99, "Classic egg kathi roll", "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300"),
            # Sushi Garden
            (17, "California Roll", "Sushi", 349, "Crab, avocado & cucumber", "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=300"),
            (17, "Dragon Roll", "Sushi", 449, "Shrimp tempura & avocado", "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=300"),
            (17, "Miso Soup", "Soups", 149, "Traditional Japanese miso soup", "https://images.unsplash.com/photo-1547592180-85f173990554?w=300"),
            (17, "Edamame", "Starters", 199, "Steamed salted soybeans", "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"),
            # The Belgian Waffle
            (18, "Classic Waffle", "Waffles", 199, "Crispy waffle with maple syrup", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300"),
            (18, "Nutella Waffle", "Waffles", 249, "Waffle with Nutella & strawberries", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300"),
            (18, "Ice Cream Waffle", "Waffles", 279, "Waffle with vanilla ice cream", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300"),
            (18, "Cold Coffee", "Beverages", 149, "Chilled creamy cold coffee", "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300"),
            # Punjabi Tadka
            (19, "Butter Chicken", "Main Course", 279, "Rich creamy butter chicken", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            (19, "Sarson Ka Saag", "Main Course", 229, "Classic Punjabi mustard saag", "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300"),
            (19, "Amritsari Kulcha", "Breads", 99, "Stuffed Amritsari bread", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300"),
            (19, "Lassi", "Beverages", 79, "Sweet chilled lassi", "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300"),
            # Noodle House
            (20, "Hakka Noodles", "Noodles", 179, "Stir fried hakka noodles", "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"),
            (20, "Fried Rice", "Rice", 169, "Wok tossed fried rice", "https://images.unsplash.com/photo-1547592180-85f173990554?w=300"),
            (20, "Manchurian", "Starters", 199, "Crispy balls in spicy sauce", "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"),
            (20, "Spring Rolls", "Starters", 149, "Crispy vegetable spring rolls", "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"),
        ]
        cursor.executemany("INSERT INTO menu_items (restaurant_id, name, category, price, description, image) VALUES (?,?,?,?,?,?)", menu_items)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            user_name TEXT,
            rating REAL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    conn.commit()
    conn.close()
