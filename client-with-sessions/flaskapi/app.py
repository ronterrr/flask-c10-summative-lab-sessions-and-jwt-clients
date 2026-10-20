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

class Logout(Resource):
    def post(self):
        if 'user_id' in session:
            session.pop('user_id')
            return {'message': 'Logged out successfully'}, 200
        return {'Error': 'unauthorized'}, 401

class NoteListResource(Resource):
    def get(self): #getting note list
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401

        user_id = session['user_id']
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        pagination = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
        notes = pagination.items

        return {
            'notes': notes_schema.dump(notes),
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }, 200

    def post(self): #posting note list
        if 'user_id' not in session:
            return {'Error': "Unatuhorized"}, 401

        data = request.get_json()
        if not data:
            return {'Error': 'No Input Data Provied'}, 400

        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'Error': 'Title and content are required'}, 400

        try:
            note = Note(title=title, content=content, user_id=session['user_id'])
            db.session.add(note)
            db.session.commit()
            return note_schema.dump(note), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400