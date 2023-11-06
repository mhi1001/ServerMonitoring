from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

app = Flask (__name__) #identify the current application or module that is being rendered or pass to Flask
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

from application import routes