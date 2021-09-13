from flask import Flask, render_template, redirect, session, flash
import requests
from werkzeug.exceptions import Unauthorized
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, bcrypt, User, FavDrink
from forms import LoginForm, RegisterForm, DrinkSearch
import os

app = Flask(__name__)

uri= os.environ.get('DATABASE_URL', "postgresql:///drinks")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


app.config['SQLALCHEMY_DATABASE_URI'] = uri


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hellosecret1')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)



db.create_all()



def get_drink_name(drink):
    """Retrieves drink data from API based on name."""

    drink_data = requests.get(f"http://thecocktaildb.com/api/json/v1/1/search.php?s={drink}")
    new_drink_data = drink_data.json()

    return new_drink_data["drinks"]





def get_drink_id(id):
    """Retrieves drink data from API based on ID."""

    drink_data = requests.get(f"http://thecocktaildb.com/api/json/v1/1/lookup.php?i={id}")
    new_drink_data = drink_data.json()

    return new_drink_data["drinks"]








@app.route('/')
def homepage():
    """Homepage of the site; redirect to register"""

    return redirect('/register')



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user: Produce form and handle submission."""


    if "username" in session:
        return redirect(f"/users/{session['username']}")

    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User.register(username, password, email)

        db.session.commit()
        session['username'] = user.username


        return redirect(f"/users/{user.username}")
    else:
        return render_template("users/register.html", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render login form and handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template('users/login.html', form=form)
    return render_template("users/login.html", form=form)



@app.route("/logout")
def logout():
    """Logout user route."""

    session.pop("username")
    return redirect("/login")



@app.route("/users/<username>")
def show_user(username):
    """Show page for logged in user."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    

    user = User.query.get(username)

    if user.favorite_drinks:
        ids = [drink.drink_id for drink in user.favorite_drinks]
    

        drinks_list = [get_drink_id(id) for id in ids]
    
    

        drink_objs = [drink for drink in drinks_list]
    

        return render_template("users/show.html", user=user, drink_objs=drink_objs)
    


    return render_template("users/show.html", user=user)



@app.route("/users/<username>/drinks", methods=['GET', 'POST'])
def handle_drinks(username):
    """Show drinks form and handle submission."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    
    form = DrinkSearch()


    if form.validate_on_submit():
        drink_name = form.drink_name.data

        drinks = get_drink_name(drink_name)


        return render_template("drinks/search_drink.html", drinks=drinks, form=form)
    
    return render_template("drinks/search_drink.html", form=form)




@app.route('/users/favDrinks/<int:drink_id>/<drink_name>', methods=['POST'])
def fav_drink(drink_id, drink_name):
        """Post favorite drink to database."""
    
        
        username = session['username']

        fav_drink = FavDrink(name=drink_name, username=username, drink_id=drink_id)
        print(fav_drink)

        db.session.add(fav_drink)
        db.session.commit()

        return redirect(f"/users/{username}/drinks")

