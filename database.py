from flask_app import db, create_app

app = create_app()

print('''1. Create Database
2. Clear Database''')

choice = int(input("Choice: "))

if choice == 1:
    db.create_all(app=app)
elif choice == 2:
    db.drop_all(app=app)
