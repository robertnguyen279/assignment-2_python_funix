from flask import Blueprint, render_template, send_from_directory, redirect, url_for
from forms import AddForm

# Initialize new blueprint
routes_page = Blueprint('routes_page', __name__, template_folder='templates')

"""
Routes start here
"""
@routes_page.route('/')
def index():
    return render_template('home.html')

@routes_page.route('/add', methods=['GET', 'POST'])
def add_new_post():
    add_post_form = AddForm()
    if add_post_form.validate_on_submit():
        return redirect(url_for('routes_page.index'))
    return render_template('add.html', form=add_post_form)

# Serve static files
@routes_page.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('templates/assets', path)

@routes_page.route('/styles/<path:path>')
def send_styles(path):
    return send_from_directory('templates/styles', path)