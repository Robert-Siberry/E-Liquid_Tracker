from flask import Flask, redirect, url_for, render_template, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
from wtforms import ValidationError
from forms import EliquidsForm, RemoveForm, RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
                                        environ.get('MYSQL_USER') + \
                                        ':' + \
                                        environ.get('MYSQL_PASSWORD') + \
                                        '@' + \
                                        environ.get('MYSQL_HOST') + \
                                        ':' + \
                                        environ.get('MYSQL_PORT') + \
                                        '/' + \
                                        environ.get('MYSQL_DB_NAME')
db = SQLAlchemy(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class eliquids(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    brand = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    flavours = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return ''.join(
            [
                'description: ' + self.description + '\n'
                'brand: ' + self.brand, + ' ' + self.name + '\n'
                'flavours: ' + self.flavours
            ]
        )




class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return ''.join(['User ID: ', str(self.id), '\r\n',
                        'Email: ', self.email, '\r\n',
                        'Name: ', self.f_name, ' ', self.l_name
                        ])




def validate_email(email):
    user = Users.query.filter_by(email=email.data).first()

    if user:
        raise ValidationError('Email already in use')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(f_name=form.f_name.data,
                     l_name=form.l_name.data,
                     email=form.email.data,
                     password=hash_pw
                     )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
@login_required
def home():
    post_data = eliquids.query.all()
    return render_template('homepage.html', description='Homepage', eliquids=post_data)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', description='About')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = EliquidsForm()
    if form.validate_on_submit():
        post_data = eliquids(
            brand=form.brand.data,
            name=form.name.data,
            description=form.description.data,
            flavours=form.flavours.data
        )
        db.session.add(post_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('post.html', description='add a post', form=form)


@app.route('/create')
def create():
    db.drop_all()
    db.create_all()
    post = eliquids(brand='Bad Drip', name='Dont Care Bear', description='A candied treat that you can enjoy all day',
                    flavours="Gummy Bears, melon and Peach")
    post2 = eliquids(brand='Strapped', name='Tangy Tutti Frutti', description='A tongue tingling take on tutti frutti',
                     flavours="Candied fruits and tangy Sherbet")
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()
    return "added a table and populated it with some info"


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = RemoveForm()
    if form.validate_on_submit():
        delete_data = eliquids(
            brand=form.brand.data,
            name=form.name.data,
            description=form.description.data,
            flavours=form.flavours.data
        )
        db.session.query(eliquids).filter_by(name=form.name.data).delete()
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('post.html', title='add a post', form=form)

if __name__ == '__main__':
    app.run()
