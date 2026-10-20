from app import app
from models import db, User, Note
from faker import Faker

fake = Faker()

def seed_database():
    with app.app_context():
        print("Clearing database adn creating tables...")
        db.drop_all()
        db.create_all()

        print("Seeding users...")
        users = []
        for i in range(5):
            user = User(
                username = fake.user_name(),
                email = fake.email()
            )
            user.password = 'password'

            db.session.add(user)
            users.append(user)

            db.session.commit()

            print('seeding notes for users...')
            for user in users:
                for i in range(4):
                    note = Note(
                        title = fake.sentence(nb_words=4),
                        content=fake.paragraph(nb_sentences=3),
                        user_id=user.id
                    )
                    db.session.add(note)

            db.session.commit()
            print('Database seeded successfully')

if __name__ == "__main__":
    seed_database()