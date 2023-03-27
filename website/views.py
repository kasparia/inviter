from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from . import db, is_valid_email, is_valid_string, generateCaptchaSequence
from .models import Visitor
from captcha.image import ImageCaptcha

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	
	if request.method == 'POST':
		print("postt")
		if request.form.get('nameField') != None and request.form.get('nameField') != "" and request.form.get('emailField') != None and request.form.get('emailField') != "" and request.form.get('codeTest') != "":
			nameFieldData = request.form.get('nameField')
			emailFieldData = request.form.get('emailField')
			captchaData = request.form.get('codeTest')

			if captchaData != None and captchaData == session['captcha']:

				if is_valid_email(emailFieldData):
					visitorEmail = Visitor.query.filter_by(visitorEmail=emailFieldData).first()
					if visitorEmail != None:
						flash("Email already registered", category='error')
						captchaImage = generateCaptchaSequence()
						return render_template("home.html", user=current_user, visitorRegistered=False, captchaImage=captchaImage)
					
					else:	
						visitorInstance = Visitor.query.filter_by(visitorEmail=emailFieldData+"\n").first()

						if visitorInstance == None and is_valid_string(nameFieldData):
							visitorInstance = Visitor()
							visitorInstance.visitorName = nameFieldData
							visitorInstance.visitorEmail = emailFieldData
							db.session.add(visitorInstance)
							db.session.commit()
							session.pop('captcha')
							flash("Registration successful", category='success')
							return render_template("home.html", user=current_user, visitorRegistered=True)
						
						else:
							flash("Invalid name given", category='error')
							session.pop('captcha')
							captchaImage = generateCaptchaSequence()
							return render_template("home.html", user=current_user, visitorRegistered=False, captchaImage=captchaImage)
								
				else:
					flash("Invalid email address", category='error')
					session.pop('captcha')
					captchaImage = generateCaptchaSequence()
					return render_template("home.html", user=current_user, visitorRegistered=False, captchaImage=captchaImage)
			else:
				flash("Please fill your info :)", category='info')
				captchaImage = generateCaptchaSequence()
				return render_template("home.html", user=current_user, visitorRegistered=False, captchaImage=captchaImage)

		else:
			flash("Please fill your info :)", category='info')
			session.pop('captcha')
			captchaImage = generateCaptchaSequence()
			return render_template("home.html", user=current_user, visitorRegistered=False, captchaImage=captchaImage)
	
	else:
		print("gettt")
		captchaImage = generateCaptchaSequence()
		return render_template("home.html", user=current_user, visitorRegistered=False, captchaImage=captchaImage)
	
@views.route('/admin', methods=['GET'])
@login_required
def admin():
	Visitors = Visitor.query.all()
	return render_template("admin.html", registrants=Visitors, user=current_user)


