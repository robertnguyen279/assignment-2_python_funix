import os
from flask import Flask, render_template, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm
from datetime import date


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'assignment2-secret'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models for flask migrations
Migrate(app, db)


"""
DB Models start here
"""
class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    subtitle = db.Column(db.Text)
    author = db.Column(db.Text)
    date_posted = db.Column(db.Text)
    content = db.Column(db.Text)

    def __init__(self, title, subtitle, author, date_posted, content):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.date_posted = date_posted
        self.content = content

    def __repr__(self):
        return '<Blog {}>'.format(self.title)

    def save(self):
        db.session.add(self)
        db.session.commit()


"""
Routes start here
"""
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_new_post():
    add_post_form = AddForm()
    if add_post_form.validate_on_submit():
        title = add_post_form.title.data
        subtitle = add_post_form.subtitle.data
        author = add_post_form.author.data
        date_posted = date.today()
        content = add_post_form.content.data

        new_blog = Blog(title, subtitle, author, date_posted, content)
        new_blog.save()
        flash('Successfully added new blog')

        add_post_form.title.data = ""
        add_post_form.subtitle.data = ""
        add_post_form.author.data = ""
        add_post_form.content.data = ""
        
    return render_template('add.html', form=add_post_form)

# Serve static files
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('templates/assets', path)

@app.route('/styles/<path:path>')
def send_styles(path):
    return send_from_directory('templates/styles', path)


if __name__ == '__main__':
    app.run(debug=True)