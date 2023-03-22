from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
from . import db, is_valid_email, is_valid_string
from .models import Registrant, Visitor

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	
	# if request.args.get('code') !=None and request.args.get('email') !=None:
	if request.args.get('nameField') !=None and request.args.get('emailField') !=None:
		# input_code = request.args.get('code')
		nameFieldData = request.args.get('nameField')
		emailFieldData = request.args.get('emailField')

		if is_valid_email(emailFieldData):
			visitorEmail = Visitor.query.filter_by(visitorEmail=emailFieldData).first()
			if visitorEmail != None:
				flash("Email already registered", category='error')
				# return render_template("register.html", user=current_user, code=input_code)
				return render_template("register.html", user=current_user)
			else:	
				# visitorInstance = Visitor.query.filter_by(visitorEmail=emailFieldData+"\n").first()
				#if is_valid_string(nameFieldData):		
				visitorInstance = Visitor.query.filter_by(visitorEmail=emailFieldData+"\n").first()
				if visitorInstance == None:
					visitorInstance = Visitor()
					visitorInstance.visitorName = nameFieldData
					visitorInstance.visitorEmail = emailFieldData
					db.session.add(visitorInstance)
					db.session.commit()
					return("Email registered!")					
				else:
					flash("Invalid code", category='error')
					return render_template("home.html", user=current_user)
						
		else:
			flash("Invalid email address", category='error')
			# return render_template("register.html", user=current_user, code=input_code)
			return render_template("register.html", user=current_user)
	else:
		#flash("Invalid code", category='error')
		return render_template("home.html", user=current_user)



	"""elif request.args.get('code') !=None:
		input_code = request.args.get('code').upper()
		if is_valid_string(input_code):
			code = Registrant.query.filter_by(invitecode=input_code+"\n").first()
		else:
			flash("Don't bother trying to h4ck m3.", category='warning')
			return render_template("home.html", user=current_user) 

		if code:
			if code.used == False:
				flash("Code correct!", category='success')
				return render_template("register.html", user=current_user, code=code.invitecode)
			else:
				flash("Code already registered!", category='error') 
				return redirect(url_for('views.home'))
		else:
			flash("Invalid code", category='error')
			return render_template("home.html", user=current_user)	
	else:
		return render_template("home.html", user=current_user)"""

@views.route('/admin', methods=['GET'])
@login_required
def admin():

	#Registrants = Registrant.query.order_by(Registrant.id).all()
	# Visitors = Visitor.query.order_by(Visitor.id).all()
	Visitors = Visitor.query.all()
	return render_template("admin.html", registrants=Visitors, user=current_user)


