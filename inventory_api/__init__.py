from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import logging

app = Flask(__name__, static_folder='build', static_url_path='')
# app.run(debug=True)
# logging.basicConfig(level=logging.DEBUG)
app.config.from_object(Config)
# change postgres -> postgresql to allow for heroku and sqlalchemy inegration
DB_URI = app.config['SQLALCHEMY_DATABASE_URI'].replace("://", "ql://", 1)
print(DB_URI)
# sys.stdout.flush()
engine = create_engine(DB_URI)

import inventory_api.views


if __name__ == '__main__':
    app.run(debug=True)