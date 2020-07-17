from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import environ
from wtforms import ValidationError
from forms import EliquidsForm, RegistrationForm, LoginForm, UpdateAccountForm, UpdatePostForm
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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
    posts = db.relationship('eliquids', backref='author', lazy=True)

    def __repr__(self):
        return ''.join(['User ID: ', str(self.id), '\r\n',
                        'Email: ', self.email, '\r\n',
                        'Name: ', self.f_name, ' ', self.l_name
                        ])


def validate_email(self, email):
    if email.data != current_user.email:
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
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
    return render_template('register.html', title='Login', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('my')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('my'))
    return render_template('login.html', title='Login', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.f_name = form.f_name.data
        current_user.l_name = form.l_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.f_name.data = current_user.f_name
        form.l_name.data = current_user.l_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    ad = Users.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('register'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html', description='Homepage')


@app.route('/about')
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
            flavours=form.flavours.data,
            author=current_user
        )
        db.session.add(post_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('post.html', description='add a post', form=form)


@app.route('/my')
def my():
    post_data = eliquids.query.filter_by(user_id=current_user.id).all()
    return render_template('my.html', description='My Eliquids', eliquids=post_data)


@app.route('/update/<int:up>', methods=['GET', 'POST'])
@login_required
def update(up):
    form = UpdatePostForm()
    eliquid = eliquids.query.filter_by(id=up).first()
    if form.validate_on_submit():
        eliquid.brand = form.brand.data
        eliquid.name = form.name.data
        eliquid.description = form.description.data
        eliquid.flavours = form.flavours.data
        db.session.commit()
        return redirect(url_for('my'))
    elif request.method == 'GET':
        form.brand.data = eliquid.brand
        form.name.data = eliquid.name
        form.description.data = eliquid.description
        form.flavours.data = eliquid.flavours

    return render_template('update.html', title='update', form=form)


# @app.route('/create')
# def create():
# db.drop_all()
#  db.create_all()
#   post = eliquids(brand='Bad Drip', name='Dont Care Bear', description='A candied treat that you can enjoy all day',
#                    flavours="Gummy Bears, melon and Peach")
# post2 = eliquids(brand='Strapped', name='Tangy Tutti Frutti', description='A tongue tingling take on tutti frutti',
#                 flavours="Candied fruits and tangy Sherbet")
# db.session.add(post)
# db.session.add(post2)
# db.session.commit()
# return "added a table and populated it with some info"


@app.route('/remove/<int:up>', methods=['GET', 'POST'])
@login_required
def remove(up):
    form = UpdatePostForm()
    eliquid = eliquids.query.filter_by(id=up).first()
    if form.validate_on_submit():
        eliquid.brand = form.brand.data
        eliquid.name = form.name.data
        eliquid.description = form.description.data
        eliquid.flavours = form.flavours.data
    db.session.delete(eliquid)
    db.session.commit()
    return redirect(url_for('my'))
