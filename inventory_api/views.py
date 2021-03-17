from inventory_api import app, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin

from .serializers import UserSchema

# CORS(app, support_credentials=True)
Base = automap_base()

# reflect the tables in the database
Base.prepare(engine, reflect=True)

# load the classes for the tables
User = Base.classes.users
Inventory = Base.classes.inventory
Category  = Base.classes.category
Product = Base.classes.product
Attribute = Base.classes.attribute

session = Session(engine)
metadata = MetaData(engine)

@app.route('/')
def index():
    return "INDEX"

@app.route('/api/addUser', methods=['POST'])
def add_user():
    user_name = request.form['user_name']
    email = request.form['email']

    if user_name != None and email != None:
        try:
            user = User(user_nm=user_name, email=email)
            session.add(user)
            session.commit()
            user_schema = UserSchema()
            serialized_user = user_schema.dump(user)
            return jsonify(serialized_user)
        except Exception as e:
            return jsonify({'Error': e})
    else:
        return jsonify({'Error': f"Username was {user_name} and email was {email}"})