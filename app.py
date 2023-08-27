from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def connect_to_mongodb():
    client = MongoClient('mongodb+srv://2409:2409@cluster0.b6wokfx.mongodb.net/?retryWrites=true&w=majority')
    db = client['auction']
    return db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        db = connect_to_mongodb()
        collection = db['products']
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        product_data = {
            'name': name,
            'description': description,
            'price': price
        }
        collection.insert_one(product_data)
        return 'Product added to database!'
    else:
        db = connect_to_mongodb()
        collection = db['products']
        products = collection.find()
        return render_template('product.html', products=products)

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = connect_to_mongodb()
        collection = db['users']
        email = request.form.get('email')
        password = request.form.get('password')
        user = collection.find_one({'email': email, 'password': password})
        if user:
            return redirect(url_for('place_bid'))
        else:
            return render_template('client.html', message='Invalid email or password')
    else:
        return render_template('client.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = connect_to_mongodb()
        collection = db['users']
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }
        collection.insert_one(user_data)
        return redirect(url_for('login', message='Registration successful!'))
    else:
        return render_template('register.html')

@app.route('/place_bid')
def place_bid():
    return render_template('place_bid.html')

if __name__ == '__main__':
    app.run(debug=True, port=1234)
