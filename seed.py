from app import app
from models import db, User


db.drop_all()
db.create_all()


user1 = User.register("treeluvr", "treeluvr123", "tree@lover.com", "Jay", "Blanchett")


user2 = User.register("naturebestfriend", "naturelover123", "nature@lover.com", "Sam", "Blanchett")


db.session.add_all([user1, user2])
db.session.commit()

