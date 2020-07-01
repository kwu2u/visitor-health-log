from app import db
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    apartment = Column(String(64))
    pw_hash = Column(String(120), nullable=False)
    role_id = Column(String(64), nullable=False)
    login_ct = Column(Integer)
    created = Column(DateTime)
    last_seen = Column(DateTime)

    def __init__(self, email, apartment, password, role_id, created):
        self.email = email
        self.apartment = apartment
        self.set_password(password)
        self.role_id = role_id
        self.created = created

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return str(self.user_name)


class Visitor(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    datetime = Column(DateTime, nullable=False)
    purpose = Column(String(120), nullable=False)
    name = Column(String(120), nullable=False)
    fever = Column(Boolean, nullable=False)
    symptoms = Column(Boolean, nullable=False)
    positive_test = Column(Boolean, nullable=False)
    quarantined = Column(Boolean, nullable=False)
    passed = Column(Boolean, nullable=False)
