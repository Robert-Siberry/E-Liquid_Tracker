from flask import Flask, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ

#my IP 77.100.120.192
#token hex aac919961fe858a46dba9c060cf7fc12
from forms import PostsForm

app = Flask(__name__)
#aac919961fe858a46dba9c060cf7fc12
#make more secure
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
#app.config['SLQALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@34.89.109.23:3306/posts'
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

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return ''.join(
            [
                'Title: ' + self.title + '\n'
                'First name: ' +self.f_name, + ' ' + self.l_name +'\n'
                'Content: ' +self.content
            ]
        )




@app.route('/')
@app.route('/home')
def home():
    post_data = Posts.query.all()
    return render_template('homepage.html', title='Homepage', posts=post_data)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PostsForm()
    if form.validate_on_submit():
        post_data = Posts(
            f_name=form.f_name.data,
            l_name=form.l_name.data,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('post.html', title='add a post', form=form)

@app.route('/create')
def create():
    db.create_all()
    post = Posts(f_name='Robert', l_name='Siberry', title='Dr', content="An interesting canning article")
    post2 = Posts(f_name='Pete', l_name='Repeat', title='Mr', content="Pete and Repeat where on a boat, Pete fell out who was left?")
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()
    return "added a table and populated it with some info"


@app.route('/delete')

def delete():
    #db.drop_all()
    db.session.query(Posts).delete()
    db.session.commit()
    return "You have deleted everything, now the world is going to end!!!!!"


if __name__ == '__main__':
    app.run()