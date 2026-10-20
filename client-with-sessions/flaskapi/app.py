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

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'Error': 'No Data provided'}, 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {'error': 'Missing required fields'}, 400

        if User.query.filter_by(username=username).first():
            return {'Error': "Username already taken"}, 400

        try:
            user = User(username=username, email=email)
            user.password = password
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user_schema.dump(user), 201
        except Exception as e:
            db.session.rollback()
            return {'Error': str(e)}, 400

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'Error': 'No data provided'}, 400

        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user_schema.dump(user), 201
        return {'Error': 'Invalid username or password'}, 400

