import os

from flask import Flask

from Routes.tamer_routes import tamer_bp
from utils.PrefixMiddleware import PrefixMiddleware

app = Flask(__name__)
app.debug = True
version = os.environ.get('version', 'v1')
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=f'/api/{version}')
app.register_blueprint(tamer_bp)

@app.route('/<name>')
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    return f'Hi, {name}'  # Press Ctrl+F8 to toggle the breakpoint.


@app.route('/')
def hello_world():
    return 'Hello World'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(os.environ.get('host', 'localhost'), os.environ.get('port', 8080), debug=app.debug)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
