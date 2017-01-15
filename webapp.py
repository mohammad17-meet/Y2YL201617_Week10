from flask import Flask, request, render_template, flash, redirect, url_for
from model import *
from flask import session as login_session
from flask import g

app = Flask(__name__)
app.secret_key ="something"

engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/')
@app.route('/inventory')
def inventory():
	items = session.query(Product).all()
	return render_template('inventory.html', items=items)

@app.route('/inventory')
def Inventory():
	inventory = session.query(Product).all()
	htmlString = ""
	for item in inventory:
		htmlString += "<p>" + item.name + "</p>" + "<p>" + item.description + "</p>" +"<p>" + item.price + "</br></br>"
	return htmlString


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash('Missing Arguments')
			redirect(url_for('login'))
		if verify_password(email, password):
			customer = session.query(Customer).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % customer.name)
			login_session['name'] = customer.name
			login_session['email'] = email
			login_session['id'] = customer.id
			return redirect(url_for('inventory'))
		else:
			# incorrect username/password
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))

@app.route('/newCustomer', methods = ['GET','POST'])
def newCustomer():
	if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        if name is None or email is None or password is None:
            flash("Your form is missing arguments")
            return redirect(url_for('newCustomer'))
        if session.query(Customer).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newCustomer'))
        customer = Customer(name = name, email=email, address = address)
        customer.hash_password(password)
        session.add(customer)
        shoppingCart = ShoppingCart(customer=customer)
        session.add(shoppingCart)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('inventory'))
    else:
        return render_template('newCustomer.html')

@app.route("/product/<int:product_id>")
def product(product_id):
	product = session.query(Product).filter_by(id=product_id).one()
	return render_template('product.html', product=product)

@app.route("/product/<int:product_id>/addToCart", methods = ['POST'])
def addToCart(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	quantity = request.form['quantity']
	product = session.query(Product).filter_by(id=product_id).one()
	shoppingCart = session.query(ShoppingCart).filter_by(customer_id=login_session['id']).one()
	# If this item is already in the shopping cart, just update the quantity
	if product.name in [item.product.name for item in shoppingCart.products]:
		assoc = session.query(ShoppingCartAssociation).filter_by(shoppingCart=shoppingCart).filter_by(product=product).one()
		assoc.quantity = int(assoc.quantity) + int(quantity)
		flash("Successfully added to Shopping Cart")
		return redirect(url_for('main'))

@app.route("/shoppingCart")
def shoppingCart():
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	shoppingCart = session.query(ShoppingCart).filter_by(customer_id=login_session['id']).one()
	return render_template('shoppingcart.html', shoppingcart=shoppingcart)


@app.route("/removeFromCart/<int:product_id>", methods = ['POST'])
def removeFromCart(product_id):
	return "To be implmented"

@app.route("/updateQuantity/<int:product_id>", methods = ['POST'])
def updateQuantity(product_id):
	return "To be implemented"

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
	return "To be implmented"

@app.route("/confirmation/<confirmation>")
def confirmation(confirmation):
	return "To be implemented"

@app.route('/logout', methods = ['POST'])
def logout():
	return "To be implmented"

if __name__ == '__main__':
	app.run(debug=True)