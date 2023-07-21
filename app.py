import os
from flask import Flask, render_template, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from forms import BlogForm
from datetime import date

# Get base dir
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__)
api = Api(app)

# App configs
app.config['SECRET_KEY'] = 'assignment2-secret'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize migration
Migrate(app, db)


"""
DB Models start here
"""
class Blog(db.Model):
    __tablename__ = 'blogs'

    # Set up columns
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
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'author': self.author,
            'date_posted': self.date_posted,
            'url': 'http://127.0.0.1:5000/post/{}'.format(self.id)
        }


"""
Routes start here
"""
@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('home.html', blogs=blogs)

@app.route('/add', methods=['GET', 'POST'])
def add_new_post():
    add_post_form = BlogForm()
    if add_post_form.validate_on_submit():
        title = add_post_form.title.data
        subtitle = add_post_form.subtitle.data
        author = add_post_form.author.data
        date_posted = date.today()
        content = add_post_form.content.data

        new_blog = Blog(title, subtitle, author, date_posted, content)
        new_blog.save()
        flash('Successfully added new blog')

        # Remove data from input elements 
        add_post_form.title.data = ""
        add_post_form.subtitle.data = ""
        add_post_form.author.data = ""
        add_post_form.content.data = ""
        
    return render_template('add.html', form=add_post_form)

@app.route('/post/<int:id>')
def get_post(id):
    post = Blog.query.get(id)
    return render_template('post.html', post=post)

@app.route('/delete')
def delete_post():
    blogs = Blog.query.all()
    return render_template('delete.html', blogs=blogs)

@app.route('/delete/<int:id>')
def delete_by_id(id):
    delete_post = Blog.query.get(id)
    if not delete_post:
        return render_template('404.html')
    db.session.delete(delete_post)
    db.session.commit()
    blogs = Blog.query.all()
    return render_template('delete.html', blogs=blogs)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    edit_form = BlogForm()
    post = Blog.query.get(id)

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.author = edit_form.author.data
        post.date_posted = date.today()
        post.content = edit_form.content.data

        post.save()
        flash('Successfully updated blog')
        
    return render_template('edit.html', form=edit_form, post=post)


    

# Serve static files
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('templates/assets', path)

@app.route('/styles/<path:path>')
def send_styles(path):
    return send_from_directory('templates/styles', path)


# Not Found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""
APIs start here
"""
class BlogAPI(Resource):
    def get(self):
        blogs = Blog.query.all()

        if not blogs:
            return {'message': 'No blogs found'}, 404
        
        formated_blogs = [blog.json() for blog in blogs]
        return formated_blogs, 400

api.add_resource(BlogAPI, '/blogs')

# Run app with debug
if __name__ == '__main__':
    app.run(debug=True)