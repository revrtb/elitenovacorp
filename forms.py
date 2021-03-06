from flask_wtf import FlaskForm
from wtforms.fields import TextField, TextAreaField, SubmitField, SelectField, PasswordField, SubmitField
from wtforms import validators, ValidationError
from lib import recaptcha2
 
class ContactForm(FlaskForm):
  name = TextField("Name",  [validators.Required()])
  email = TextField("Email",  [validators.Required()])
  subject = TextField("Subject",  [validators.Required()])
  message = TextAreaField("Message",  [validators.Required()])
  website = TextField("website")
  recaptcha = recaptcha2.RecaptchaField()
  submit = SubmitField(label="Submit")

class SignUpForm(FlaskForm):
  fname = TextField("FirstName",  [validators.Required()])
  lname = TextField("LastName",  [validators.Required()])
  skype = TextField("Skype",  [validators.Required()])
  website = TextField("website", [validators.Required()])
  username = TextField("Username",  [validators.Required()])
  email = TextField("Email",  [validators.Required()])
  password = PasswordField("Password",  [validators.DataRequired(), validators.EqualTo('repassword', message='Passwords must match')])
  repassword = PasswordField("Repassword",  [validators.Required()])
  account_type = SelectField("AccountType", choices = [('adv', 'Advertiser'), ('pub', 'Publisher')])
  submit = SubmitField("Send")
  recaptcha = recaptcha2.RecaptchaField()
