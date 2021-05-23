from flask_app import db

print('''1. Create Database
2. Clear Database''')

choice = int(input("Choice: "))

if choice == 1:
    db.create_all()
elif choice == 2:
    db.drop_all()
