from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))

class Registrant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invitecode = db.Column(db.String(150), unique=True)
	reg_email = db.Column(db.String(150), unique=True)
	used = db.Column(db.Boolean(False))
	
class Visitor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	visitorName = db.Column(db.String(150), unique=True)
	visitorEmail = db.Column(db.String(150), unique=True)