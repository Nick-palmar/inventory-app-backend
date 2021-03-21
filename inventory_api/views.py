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
multiple_inventory_schema = InventorySchema(many=True)

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
            session['user_id'] = str(user.user_id)
        
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
            session['user_id'] = str(user.user_id)
            return jsonify(serialized_user), 201
        except Exception as e:
            # error because email is already taken
            db_session.rollback()
            return jsonify({'Bad Request': 'Email already exists!'}), 400
    else:
        return jsonify({'Bad Request': "User name or email were none"}), 400

@app.route('/api/sign-in', methods=['POST'])
def sign_in():
    email = request.form['email']

    if email != None:
        # check if the email exists (ignore the session data; in session will check for this)
        db_user = db_session.query(User).filter(User.email == email).first()
        if db_user != None:
            serialized_user = user_schema.dump(db_user)
            session['user_name'] = db_user.user_nm
            session['email'] = db_user.email 
            session['user_id'] = str(db_user.user_id)
            print(type(session['user_id']))
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
    if session.get('email') != email and email != None:
        return jsonify({'Not in session': 'Leave at home page'}), 404
    else:
        # user is in the session, return all user info
        user = db_session.query(User).filter(User.email == email).first()
        serialized_user = user_schema.dump(user)
        return jsonify(serialized_user), 200

@app.route('/api/view-all-users', methods=['GET'])
def get_all_users():
    all_users = db_session.query(User).all()
    return_dict = {}

    for i in range(len(all_users)):
        return_dict[f'user_{i}'] = [all_users[i].user_id, all_users[i].user_nm, all_users[i].email]
        # print(all_users)
    
    return jsonify(dict(sorted(return_dict.items()))), 200

@app.route('/api/add-inventory', methods=['POST'])
def create_inventory():
    current_user_id = request.form.get('user_id')
    inventory_name = request.form.get('inventory_name')
    # print(session.get('user_id'), current_user_id)

    if current_user_id != None and session.get('user_id') == current_user_id and inventory_name != None and inventory_name != "":
        # check if the user exists in the db Session 
        user = db_session.query(User).filter(User.user_id == current_user_id).first()
        # check that the inventory with the same name is not being created
        inventory = db_session.query(Inventory).filter(and_(Inventory.inventory_nm == inventory_name, Inventory.user_id == current_user_id)).first()
        if user != None and inventory == None:
            try:
                inventory = Inventory(user_id=current_user_id, inventory_nm=inventory_name)
                db_session.add(inventory)
                db_session.commit()
                serialized_inventory = inventory_schema.dump(inventory)
                return jsonify(serialized_inventory), 201

            except:
                # invalid session addition
                db_session.rollback()
                return jsonify({'Bad Request': 'Error in creating inventory'}), 400
        else:
            if user == None and inventory != None:
                return jsonify({'Bad Request': 'User Id and inventory were invalid'}), 400
            elif user == None:
                return jsonify({'Bad Request': 'User Id was not found'}), 404
            else:
                return jsonify({'Already Exists': 'Inventory already exists'}), 200

    else:
        if current_user_id == None:
            return jsonify({'Bad Request': 'User Id DNE'}), 404
        elif inventory_name == None or inventory_name == "":
            return jsonify({'Bad Request': 'Inventory Name was not given'}), 400
        else:
            return jsonify({'Bad Request': 'This user id was not in session'}), 403


@app.route('/api/get-inventories', methods=['GET'])
def get_user_inventories():
    user_id = request.args.get('user_id')
    
    if user_id != None and session.get('user_id') == user_id:
        user_inventories = db_session.query(Inventory).filter(Inventory.user_id == user_id).all()

        if user_inventories != None:
            serialized_inventories = multiple_inventory_schema.dump(user_inventories)
            return jsonify(serialized_inventories), 200
        else:
            return jsonify({'Not found': 'No inventories found'}), 200
    else:
        if user_id == None:
            return jsonify({'Bad Request': 'No User ID passed'}), 400
        else:
            return jsonify({'Bad Request': 'User not in session'}), 403


@app.route('/api/delete-inventory/<user_id>/<inventory_name>', methods=['DELETE'])
def remove_inventory(user_id, inventory_name):
    print(user_id, inventory_name)
    if user_id != None and user_id != '' and inventory_name != None and inventory_name != '' and session.get('user_id') == user_id:
        # An in session user id and inventory name was passed, try to delete
        inventory = db_session.query(Inventory).filter(and_(Inventory.user_id == user_id, Inventory.inventory_nm == inventory_name)).first()
        if inventory != None:
            # to_delete = db_session.query(Inventory).filter(and_(Inventory.user_id == user_id, Inventory.inventory_nm == inventory_name)).delete(synchronize_session='fetch')
            # print(inventory_schema.dump(to_delete))
            db_session.delete(inventory)
            db_session.commit()
            return jsonify({'Accepted': f'{inventory_name} inventory was deleted'}), 204
        else:
            # user id and inventory not found - they do not match
            db_session.rollback()
            return jsonify({'Not Found': f'Inventory with user id {user_id} and name \'{inventory_name}\' was not found'}), 404
    else:
        if user_id == None or user_id == '':
            return jsonify({'Not Found': 'User is empty'}), 404
        elif session.get('user_id') != user_id:
            return jsonify({'Unauthorized': 'This user is not in session and cannot delete and inventory'}), 403
        else:
            return jsonify({'Not Found': 'The inventory name is empty'}), 404
    



