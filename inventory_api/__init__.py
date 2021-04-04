from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import logging

app = Flask(__name__)
# app.run(debug=True)
# logging.basicConfig(level=logging.DEBUG)
app.config.from_object(Config)
print(app.config['SQLALCHEMY_DATABASE_URI'])
sys.stdout.flush()
DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)

import inventory_api.views


if __name__ == '__main__':
    app.run(debug=True)