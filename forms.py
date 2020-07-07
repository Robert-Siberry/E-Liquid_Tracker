from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PostsForm(FlaskForm):
    f_name = StringField(
        'Brand',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    l_name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    title = StringField(
        'Description',
        validators=[
            DataRequired(),
            Length(min=10, max=100)
        ]
    )

    content = StringField(
        'Flavours',
        validators=[
            DataRequired(),
            Length(min=4, max=300)
        ]
    )

    submit = SubmitField('Submit a Post')
