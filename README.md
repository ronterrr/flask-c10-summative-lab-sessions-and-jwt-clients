# NOTES MANAGER API
This is a lightweight Flask REST API using Flask-RESTful, SQLAlchemy, Marshmallow and Session Auth for managing user accounts and personal notes.

## HOW TO RUN
1. Run `pipenv install`
2. Run `pipenv shell`
3. Run `flask db upgrade`
4. Run `python seed.py`
5. Run `python app.py`

## API ENDPOINTS
`POST /signup` - Registers a new user
`POST /login` - Authenticates a user and starts a session
`POST /logout` - Destroys the current user session
`GET /notes` - Lists all notes for the logged-in user
`POST /notes` - Creates a new note (provide the title and content)
`GET /notes/<id>` - Retrieves a specific note by ID
`PATCH /notes/<id>` - Updates a specific note
`DELETE /notes/<id>` - Deletes a specific note

## TEST DATA
1. Seeded Users (Generated using `seed.py`)
   - The seed script creates 5 random users using Faker.
   - All seeded users share the default password: `password`
  
### Sample JSON Data for API testing
User Signup/Login:

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "johndoe123"
}

Create Note:

{
  "title": "Demo Note", 
  "content": "This is an example of a note"
}
