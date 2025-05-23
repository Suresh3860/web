from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_from_directory
import os
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  
app.secret_key = 'your_secret_key_here'


users = {
    'admin': generate_password_hash('admin123'),
    'user1': generate_password_hash('password1')
}


milkshakes = [
    {"id": 1, "name": "Chocolate Dream", "price": 5.99, "image": "chocolate-milkshake.jpg", "description": "Rich chocolate flavor with whipped cream"},
    {"id": 2, "name": "Vanilla Bliss", "price": 4.99, "image": "vanilla-milkshake.jpg", "description": "Classic vanilla with a hint of caramel"},
    {"id": 3, "name": "Strawberry Delight", "price": 5.49, "image": "strawberry-milkshake.jpg", "description": "Fresh strawberries blended to perfection"}
]

snacks = [
    {"id": 4, "name": "Cheese Nachos", "price": 6.99, "image": "nachos.jpg", "description": "Crispy nachos with melted cheese"},
    {"id": 5, "name": "Chicken Wings", "price": 8.99, "image": "wings.jpg", "description": "Spicy buffalo wings with blue cheese dip"},
    {"id": 6, "name": "Onion Rings", "price": 4.49, "image": "onion-rings.jpg", "description": "Golden crispy onion rings"}
]


products = milkshakes + snacks

@app.route('/')
def home():
    
    testimonials = [
        {"name": "Alex", "text": "Best milkshakes in town! The Chocolate Dream is my favorite."},
        {"name": "Jamie", "text": "Love the snacks here. Perfect place to hang out with tech friends."},
        {"name": "Taylor", "text": "Great atmosphere and even better food. Highly recommended!"},
        {"name": "Morgan", "text": "The Vanilla Bliss is to die for. Comes here every weekend!"}
    ]
    
    
    displayed_testimonials = random.sample(testimonials, 3)
    
    return render_template('index.html', 
                         products=products,
                         testimonials=displayed_testimonials,
                         logged_in='username' in session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':  
    
    os.makedirs('static/images', exist_ok=True)
    app.run(debug=True)