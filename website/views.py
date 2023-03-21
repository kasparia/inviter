from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
from . import db, is_valid_email, is_valid_string
from .models import Registrant

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	
	if request.args.get('code') !=None and request.args.get('email') !=None:
		input_code = request.args.get('code')
		input_email = request.args.get('email')

		if is_valid_email(input_email):
			email = Registrant.query.filter_by(reg_email=input_email).first()
			if email != None:
				flash("Email already registered", category='error')
				return render_template("register.html", user=current_user, code=input_code)
			else:	
				code = Registrant.query.filter_by(invitecode=input_code+"\n").first()
				if code:					
					code.reg_email = input_email
					code.used = True
					db.session.commit()
					return("Email registered!")					
				else:
					flash("Invalid code", category='error')
					return render_template("home.html", user=current_user)
						
		else:
			flash("Invalid email address", category='error')
			return render_template("register.html", user=current_user, code=input_code)


	elif request.args.get('code') !=None:
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
		return render_template("home.html", user=current_user)

@views.route('/admin', methods=['GET'])
@login_required
def admin():

	#Registrants = Registrant.query.order_by(Registrant.id).all()
	Registrants = Registrant.query.filter_by(used=True).order_by(Registrant.id).all()
	return render_template("admin.html", registrants=Registrants, user=current_user)


