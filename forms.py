from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """User Registration Form."""


    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=100)])

    email = StringField("Email", validators=[InputRequired(), Length(max=50), Email()])



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=100)])



class DrinkSearch(FlaskForm):
    """Search for drinks."""


    drink_name = StringField("Drink", validators=[InputRequired()])