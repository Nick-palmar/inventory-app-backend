from inventory_api import app
from flask_marshmallow import Marshmallow

# add marshmallow for serializing to json
ma = Marshmallow(app)

# serialize data to be return through json

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_nm', 'email')

class InventorySchema(ma.Schema):
    class Meta:
        fields = ('inventory_id', 'user_id', 'inventory_nm', 'created_at')