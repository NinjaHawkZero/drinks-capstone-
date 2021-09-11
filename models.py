from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app"""

    db.app= app
    db.init_app(app)





class User(db.Model):
    """Model for users."""

    __tablename__ = "users"

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    favorite_drinks = db.relationship("FavDrink", backref="user", cascade = "all, delete")


    @classmethod
    def register(cls, username, password, email):
        """Register a user, hashing their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_decode = hashed.decode("utf8")
        user = cls(username=username, password=hashed_decode, email=email )

        db.session.add(user)

        return user

    
    @classmethod
    def authenticate(cls, username, password):
        """Validates user and password"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class FavDrink(db.Model):
    """Favorite drinks."""

    __tablename__ = "FavDrink"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    drink_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)


