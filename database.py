from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'some_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groceries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(100))

    def __repr__(self):
        return 'Grocery(id={}, name={}, price={}, image_url={})'.format(
            self.id, self.name, self.price, self.image_url)


"""

db.create_all()

grocery1 = Grocery(name='RETRO ENGLAND FOOTBALL KIT', price=149.99,image_url ="./images/england.jpg")
grocery2 = Grocery(name='RETRO ARSENAL FOOTBALL KIT', price=130,image_url ="./images/arsenal.jpg")
grocery3 = Grocery(name='RETRO BRAZIL FOOTBALL KIT', price=150.50,image_url ="./images/brazil.jpg")
grocery4 = Grocery(name='SIGNED MESSI SHIRT', price=300,image_url ="./images/messi.jpg")
grocery5 = Grocery(name='RETRO FOOTBALL BOOTS', price=220,image_url ="./images/boots.jpg")
grocery6 = Grocery(name='SIGNED RONALDO FOOTBALL BOOTS', price=425.50,image_url ="./images/ronaldo.jpg")


db.session.add_all([grocery1, grocery2, grocery3,grocery4,grocery5,grocery6])
db.session.commit()
"""




@app.route('/')
def index():
    groceries = Grocery.query.all()
    return render_template('home.html', groceries=groceries)

@app.route('/products')
def products():
    groceries = Grocery.query.all()
    return render_template('products.html', groceries=groceries)

@app.route('/sort_price')
def sort_by_price():
    products = Grocery.query.all()
    sorted_products = sorted(products, key=lambda k: k.price)
    return render_template('products_price.html', sorted_products=sorted_products)

@app.route('/sort_name')
def sort_by_name():
    products = Grocery.query.all()
    sorted_products = sorted(products, key=lambda k:k.name)
    return render_template('products_price.html', sorted_products=sorted_products)


@app.route('/checkout')
def checkout():
    groceries = Grocery.query.all()
    session.pop('basket', None)
    session['basket_count'] = 0

    
    return render_template('checkout.html' ,groceries=groceries)
    
    


def basket_total(basket):
    total = 0
    for item in basket:
        total += item['price']
        
    return total


@app.route('/basket')
def basket():
    groceries = Grocery.query.all()
    for grocery in groceries:
        grocery.price = float(grocery.price)

    db.session.commit()
    basket = session.get('basket', [])
    total = basket_total(basket)
    return render_template('basket.html', basket=basket, total=total)

@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    product = Grocery.query.get_or_404(product_id)

    if 'basket' not in session:
        session['basket'] = []

    basket = session['basket']
    basket.append(grocery_to_dict(product))

    session['basket_count'] = len(basket)
    session.modified = True

    #flash(f"{product.name} added to basket!")
    return redirect(url_for('products'))
    
def grocery_to_dict(grocery):
    return {'id': grocery.id, 'name': grocery.name, 'price': grocery.price, 'image_url': grocery.image_url}


@app.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    product_id = request.form.get('product_id')
    if 'basket' in session:
        basket = session['basket']
        for item in basket:
            if item['id'] == int(product_id):
                basket.remove(item)
                session['basket_count'] = len(basket)
                session.modified = True
                break
    return redirect(url_for('basket'))


@app.route('/view/1')
def view_product1():
    return render_template('product_details_1.html')

@app.route('/view/2')
def view_product2():
    return render_template('product_details_2.html')


@app.route('/view/3')
def view_product3():
    return render_template('products_details_3.html')


@app.route('/view/4')
def view_product4():
    return render_template('product_details_4.html')



@app.route('/view/5')
def view_product5():
    return render_template('product_details_5.html')


@app.route('/view/6')
def view_product():
    return render_template('product_details_6.html')

if __name__ == '__main__':
    app.run(debug=True)





























    















    
