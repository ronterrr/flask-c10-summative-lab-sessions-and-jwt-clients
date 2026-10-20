import os
from flask import Flask, request, session
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, bcrypt, User, Note, UserSchema, NoteSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_session_key')

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

user_schema = UserSchema()
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)