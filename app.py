from flask import Flask
from route import routes_page

app = Flask(__name__)

# Register routes from seperate route file
app.register_blueprint(routes_page)


if __name__ == '__main__':
    app.run(debug=True)