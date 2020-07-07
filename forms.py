from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


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
