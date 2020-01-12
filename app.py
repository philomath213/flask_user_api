from flask import Flask

from model import db
from auth import auth_bp
from flag import flag_bp


app = Flask(__name__)

# load the instance config
app.config.from_pyfile('config.py')

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(flag_bp, url_prefix='/flag')


if __name__ == '__main__':
    app.run(debug=True)
