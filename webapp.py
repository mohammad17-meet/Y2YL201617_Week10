from flask import Flask, request, render_template, flash, redirect, url_for
from model import *
from flask import session as login_session
from flask import g


app = Flask(__name__)
app.secret_key ="something"

engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def verify_password(email, password):
	customer = session/query(Customer).filter_by(email=email).first()
	if not customer or not customer.verify_password(password):
			return False
	else:
		return True
	pass


@app.route("/")
def home():



	return render_template("home.html")

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
			return redirect(url_for('players'))
		else:
			# incorrect username/password
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))

@app.route('/newuser', methods = ['GET','POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name is None or email is None or password is None:
            flash("Your form is missing arguments")
            return redirect(url_for('newuser'))
        if session.query(Person).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newuser'))
       	user = Person(name = name, email=email)
        session.add(user)
        My_team = Myteam(player_id=user.id)
        session.add(My_team)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('players'))
    else:
        return render_template('newuser.html')



@app.route('/players')
def players():
	items = session.query(Player).all()
	return render_template('players.html', items=items)

#@app.route('/inventory')
#def Inventory():
#	inventory = session.query(Product).all()
#	htmlString = ""
#	for item in inventory:
#		htmlString += "<p>" + item.name + "</p>" + "<p>" + item.description + "</p>" +"<p>" + item.price + "</br></br>"
#	return htmlString

@app.route("/removefromteam/<int:player_id>", methods=["POST"])
def removefromteam():
	if 'id' not in login_session:
		flash("u have to be ")
		pass
	pass




@app.route("/player/<int:player_id>/addToTeam", methods = ['POST'])
def addToTeam(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	quantity = request.form['quantity']
	player = session.query(Player).filter_by(id=player_id).one()
	Myteam = session.query(ShoppingCart).filter_by(customer_id=login_session['id']).one()
	# If this item is already in the shopping cart, just update the quantity
	if player.name in [item.player.name for item in Myteam.player]:
		assoc = session.query(MyteamAssociation).filter_by(myteam=myteam).filter_by(player=player).one()
		assoc.quantity = int(assoc.quantity) + int(quantity)
		flash("Successfully added to your team")
		return redirect(url_for('main'))




if __name__ == '__main__':
	app.run(debug=True)