import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash 

class User(db.Document):
    user_id = db.IntField (unique = True)
    first_name = db.StringField (max_length = 55)
    last_name = db.StringField (max_length = 55)
    email = db.EmailField (max_length = 30, unique = True)         #validate the email represantation
    password = db.StringField () #no length set as the hashing generates a 128 char long

    #hash password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    #un-hash password
    def get_password(self, password):
        return check_password_hash (self.password, password)

class Server (db.Document):
    serial_no = db.StringField (unique = True)
    ip_address = db.StringField (max_length = 35)
    up_time = db.IntField
    product_name = db.StringField (max_length = 50)
    temperature = db.StringField (max_length = 10)
    power_average = db.IntField
    power_current = db.IntField
    power_min = db.IntField 
    power_max = db.IntField 
    status = db.StringField (max_length = 4)
