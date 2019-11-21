from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

user_promotion = db.Table('user_promotion',
    db.Column('id_user', db.Integer, db.ForeignKey('user.id_user')),
    db.Column('id_promotion', db.Integer, db.ForeignKey('promotion.id_promotion'))
)

class User(UserMixin,db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(45), index=True, unique=True, nullable=False)
    lastname = db.Column(db.String(45), index=True, unique=True, nullable=False)
    username = db.Column(db.String(45), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), index=True, nullable=False)
    birthday = db.Column(db.Date, index=True, nullable=True)
    promotion = db.relationship('Promotion', secondary=user_promotion, backref=db.backref('promotions', lazy = 'dynamic'))

    def get_id(self):
        return (self.id_user)

    def __repr__(self):
        return '<User {}>'.format(self.firstname, self.lastname, self.username, self.email, self.birthday)    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Promotion(db.Model):
    id_promotion = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), index=True, unique=True, nullable=False)
    promotion = db.Column(db.String(45), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<Promotion {}>'.format(self.promotion)   

