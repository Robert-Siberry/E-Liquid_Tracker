from flask import Flask, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ

# my IP 77.100.120.192
# token hex aac919961fe858a46dba9c060cf7fc12
from forms import EliquidsForm

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


@app.route('/')
@app.route('/home')
def home():
    post_data = eliquids.query.all()
    return render_template('homepage.html', description='Homepage', eliquids=post_data)


@app.route('/about')
def about():
    return render_template('about.html', description='About')


@app.route('/add', methods=['GET', 'POST'])
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
    db.create_all()
    post = eliquids(brand='Bad Drip', name='Dont Care Bear', description='A candied treat that you can enjoy all day',
                    flavours="Gummy Bears, melon and Peach")
    post2 = eliquids(brand='Strapped', name='Tangy Tutti Frutti', description='A tongue tingling take on tutti frutti',
                     flavours="Candied fruits and tangy Sherbet")
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()
    return "added a table and populated it with some info"


#@app.route('/delete')
#def delete():
    #db.drop_all()
    #db.session.query(eliquids).delete()
    #db.session.commit()
    #return "You have deleted everything, now the world is going to end!!!!!"


if __name__ == '__main__':
    app.run()
