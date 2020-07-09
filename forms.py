from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class EliquidsForm(FlaskForm):
    brand = StringField(
        'Brand',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    description = StringField(
        'Description',
        validators=[
            DataRequired(),
            Length(min=10, max=1000)
        ]
    )

    flavours = StringField(
        'Flavours',
        validators=[
            DataRequired(),
            Length(min=10, max=100)
        ]
    )

    submit = SubmitField('Add a new E-Liquid')


class RemoveForm(FlaskForm):
    brand = StringField(
        'Brand',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    description = StringField(
        'Description',
        validators=[
            DataRequired(),
            Length(min=10, max=1000)
        ]
    )

    flavours = StringField(
        'Flavours',
        validators=[
            DataRequired(),
            Length(min=10, max=100)
        ]
    )

    submit = SubmitField('Remove an E-Liquid')


class RegistrationForm(FlaskForm):
    f_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    l_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')