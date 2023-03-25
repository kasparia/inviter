from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db, is_valid_email, is_valid_string
from .models import Visitor

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():

	if request.args.get('nameField') != None and request.args.get('nameField') != "" and request.args.get('emailField') != None and request.args.get('emailField') != "":
		nameFieldData = request.args.get('nameField')
		emailFieldData = request.args.get('emailField')

		if is_valid_email(emailFieldData):
			visitorEmail = Visitor.query.filter_by(visitorEmail=emailFieldData).first()
			if visitorEmail != None:
				flash("Email already registered", category='error')
				return render_template("home.html", user=current_user, nameField=nameFieldData, emailField=emailFieldData)
			else:	

				visitorInstance = Visitor.query.filter_by(visitorEmail=emailFieldData+"\n").first()
				if visitorInstance == None and is_valid_string(nameFieldData):
					visitorInstance = Visitor()
					visitorInstance.visitorName = nameFieldData
					visitorInstance.visitorEmail = emailFieldData
					db.session.add(visitorInstance)
					db.session.commit()
					flash("Registration successful", category='success')
					return render_template("home.html", user=current_user, visitorRegistered=True)
				
				else:
					flash("Invalid name given", category='error')
					return render_template("home.html", user=current_user, visitorRegistered=False)
						
		else:
			flash("Invalid email address", category='error')
			return render_template("home.html", user=current_user, visitorRegistered=False)
	else:
		flash("Please fill your info :)", category='info')
		return render_template("home.html", user=current_user, visitorRegistered=False)


@views.route('/admin', methods=['GET'])
@login_required
def admin():
	Visitors = Visitor.query.all()
	return render_template("admin.html", registrants=Visitors, user=current_user)


