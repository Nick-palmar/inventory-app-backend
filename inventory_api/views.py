from inventory_api import app, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify, session, Response
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

# create all schemas 
user_schema = UserSchema()

@app.route('/')
def index():
    return "INDEX"

def validate_entire_entry(object, *all_fields, **entered_values) -> bool:
    """ Ensure that all fields are matching with a database or session

    Args:
        object: An object of any type in the database schema (matches with any table)
        *all_fields: Var length argument that validates a certain type of object from a table in the db
        **entered_values: The values entered by the person
    
    Returns:
        True if the exact item exist, false otherwise
    """
    for col in all_fields:
        if object.col != entered_values[col]:
            return False 
    return True

@app.route('/api/sign-up', methods=['POST'])
def sign_up():
    user_name = request.form['user_name']
    email = request.form['email']

    # make sure that the user DNE
    user = User.query.filter_by(email=email).first()
    user_exists = validate_entire_entry(user, *['user_name', 'email'], user_name=user_name, email=email)

    # check if the current user is a valid user
    if user_exists:
        if 'email' not in session:
            session['user_name'] = user.user_name
            session['email'] = user.email 
            session['user_id'] = user.user_id
        
        return jsonify({'Already Exists': f'{session['email']} already exists in db'}), 200

    # user is either invalid or does not yet exist
    if user_name != None and email != None:
        try:
            # try to create the user and add it
            user = User(user_nm=user_name, email=email)
            session.add(user)
            session.commit()
            serialized_user = user_schema.dump(user)
            return jsonify(serialized_user), 201
        except Exception as e:
            # error because email is already taken
            return jsonify({'Error': e}), 400
    else:
        return jsonify({'Bad Request': f"User name or email were none"}), 400

# @app.route('/api/sign-in', methods=['POST'])
# def sign_in():
#     user_name = request.form['user_name']
#     email = request.form['email']

#     if user_name != None and email != None:
#         try:
#             user = User(user_nm=user_name, email=email)
#             session.add(user)
#             session.commit()
#             serialized_user = user_schema.dump(user)
#             return jsonify(serialized_user)
#         except Exception as e:
#             return jsonify({'Error': e})
#     else:
#         return jsonify({'Error': f"Username was {user_name} and email was {email}"}), 201

@app.route('/api/in-session', methods=['GET'])
def check_user_session():
    email = request.args.get('email')
    # check if the user is currently in a session by checking for unique emails
    if 'email' not in session:
        return jsonify({'Not in session': 'Leave at home page'}), 404
    else:
        # user is in the session, return all user info
        user = User.query.filter_by(email=email).first()
        serialized_user = user_schema.dump(user)
        return jsonify(serialized_user), 200


