from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EliquidsForm(FlaskForm):
    brand = StringField(
        'brand',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    description = StringField(
        'description',
        validators=[
            DataRequired(),
            Length(min=10, max=1000)
        ]
    )

    flavours = StringField(
        'flavours',
        validators=[
            DataRequired(),
            Length(min=10, max=100)
        ]
    )

    submit = SubmitField('Add a new E-Liquid')
