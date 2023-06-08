from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20),primary_key=True, nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    email =db.Column(db.String(50), nullable=False)
    first_name=db.Column(db.String(30), nullable=False)
    last_name=db.Column(db.String(30), nullable=False)
    created_at=db.Column(db.DateTime, default =datetime.now)

    visits = db.relationship("Visit", backref="user", passive_deletes=True)
  

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email= email, first_name = first_name, last_name=last_name )

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """ 

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False

class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True, nullable=False,  unique=True)
    start_date =db.Column(db.Date, nullable=False)
    end_date=db.Column(db.Date, nullable=False)
    park_code = db.Column(db.String(4), db.ForeignKey('parks.park_code', ondelete='CASCADE'))
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete='CASCADE'))

    
    activities = db.relationship("Activity", backref="visit", passive_deletes=True)

class Park(db.Model):
    __tablename__ = 'parks'
    park_code = db.Column(db.String(4),primary_key=True, nullable=False,  unique=True)
    park_name = db.Column(db.Text, nullable = False)

    visits = db.relationship("Visit", backref="park", passive_deletes=True)


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key= True, nullable=False,  unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    duration = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    visit_id = db.Column(db.Integer, db.ForeignKey('visits.id', ondelete='CASCADE'))