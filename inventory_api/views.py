from inventory_api import app, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify, Response, session
# print(type(session))
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin

from .serializers import UserSchema, InventorySchema

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

db_session = Session(engine)
# print(type(session))
metadata = MetaData(engine)

# create all schemas 
user_schema = UserSchema()
inventory_schema = InventorySchema()

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
        if getattr(object, col) != entered_values[col]:
            return False 
    return True

@app.route('/api/sign-up', methods=['POST'])
def sign_up():
    user_name = request.form['user_name']
    email = request.form['email']
    print(email)

    # make sure that the user DNE
    user = db_session.query(User).filter(User.email == email).first()
    if user:
        user_exists = validate_entire_entry(user, *['user_nm', 'email'], user_nm=user_name, email=email)
    else:
        user_exists = False

    # check if the current user is a valid user
    if user_exists:
        if 'email' not in session:
            session['user_name'] = user.user_nm
            session['email'] = user.email 
            session['user_id'] = user.user_id
        
        return jsonify({'Already Exists': f'{user.email} already exists in db'}), 200

    # user is either invalid or does not yet exist
    if user_name != None and email != None:
        try:
            # try to create the user and add it
            user = User(user_nm=user_name, email=email)
            db_session.add(user)
            db_session.commit()
            serialized_user = user_schema.dump(user)
            session['user_name'] = user.user_nm
            session['email'] = user.email 
            session['user_id'] = user.user_id
            return jsonify(serialized_user), 201
        except Exception as e:
            # error because email is already taken
            db_session.rollback()
            return jsonify({'Bad Request': 'Email already exists!'}), 400
    else:
        return jsonify({'Bad Request': f"User name or email were none"}), 400

@app.route('/api/sign-in', methods=['POST'])
def sign_in():
    email = request.form['email']

    if email != None:
        # check if the email exists (ignore the session data; in session will check for this)
        db_user = db_session.query(User).filter(User.email == email).first()
        if db_user != None:
            serialized_user = user_schema.dump(db_user)
            session['user_name'] = user.user_nm
            session['email'] = user.email 
            session['user_id'] = user.user_id
            return jsonify(serialized_user), 200
        else:
            return jsonify({'Bad Request': 'Email DNE'}), 404
    else:
        return jsonify({'Bad Request': "Email was none"}), 404

@app.route('/api/in-session', methods=['GET'])
def check_user_session():
    email = request.args.get('email')
    print(session.get('email'))
    # check if the user is currently in a session by checking for unique emails in the session
    if session.get('email') != email:
        return jsonify({'Not in session': 'Leave at home page'}), 404
    else:
        # user is in the session, return all user info
        user = db_session.query(User).filter(User.email == email).first()
        serialized_user = user_schema.dump(user)
        return jsonify(serialized_user), 200

@app.route('/api/view-all', methods=['GET'])
def get_all_users():
    all_users = db_session.query(User).all()
    return_dict = {}

    for i in range(len(all_users)):
        return_dict[f'user_{i}'] = [all_users[i].user_id, all_users[i].user_nm, all_users[i].email]
        print(all_users)
    
    return jsonify(return_dict), 200

@app.route('/api/add-inventory', methods=['POST'])
def create_inventory():
    current_user_id = request.form.get('user_id')
    inventory_name = request.form.get('inventory_name')

    if current_user != None:
        # check if the user exists in the db Session 
        user = db_session.query(User).filter(User.user_id == current_user_id).first()
        # check that the inventory with the same name is not being created
        inventory = db_session.query(Inventory).filter(Inventory.inventory_nm == inventory_name).first()
        if user != None and inventory == None:
            try:
                inventory = Inventory(user_id=current_user_id, inventory_nm=inventory_name)
                db_session.add(inventory)
                db_session.commit()
                # continue work here 

            except:
                # invalid session addition
                db_session.rollback()
                return jsonify({'Bad Request': 'User Id DNE'}), 404
        else:
            if user == None and inventory != None:
                return jsonify({'Bad Request': 'User Id and inventory were invalid'}), 400
            elif user == None:
                return jsonify({'Bad Request': 'User Id was not found'}), 404
            else:
                return jsonify({'Bad Request': 'Inventory already exists'}), 400

    else:
        return jsonify({'Bad Request': 'User Id DNE found'}), 404



    



