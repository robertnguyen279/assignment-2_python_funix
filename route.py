from flask import Blueprint, render_template, send_from_directory

# Initialize new blueprint
routes_page = Blueprint('routes_page', __name__, template_folder='templates')

@routes_page.route('/')
def index():
    return render_template('home.html')


# Serve static files
@routes_page.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('templates/assets', path)

@routes_page.route('/styles/<path:path>')
def send_styles(path):
    return send_from_directory('templates/styles', path)