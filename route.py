from flask import Blueprint, render_template, send_from_directory

routes_page = Blueprint('simple_page', __name__, template_folder='templates')

@routes_page.route('/')
def index():
    return render_template('home.html')



# Serve asset files
@routes_page.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('templates/assets', path)