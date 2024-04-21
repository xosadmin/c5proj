from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Passwrd', validators=[DataRequired()])
    pin_code = PasswordField('PIN Code', validators=[DataRequired()])
    submit = SubmitField('Register')

class ForgetPassword(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    pin_code = PasswordField('PIN Code', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class signEmotionForm(FlaskForm):
    feelings = StringField('Your Feelings (e.g. Happy/Angry)')
    comments = StringField('Comments')
    submit = SubmitField('Save')

class modifyPassword(FlaskForm):
    new_password = PasswordField("New Password")
    repeat_newpassword = PasswordField("Repeat New Password")
    pin_code = PasswordField("PIN Code")
    submit = SubmitField("Change Password")

class modifyPinCode(FlaskForm):
    old_pin = PasswordField("Old PIN Number")
    new_pin = PasswordField("New PIN")
    repeat_newpin = PasswordField("Repeat New PIN")
    submit = SubmitField("Change PIN")

class newRequest(FlaskForm):
    title = StringField("Request Title")
    contents = StringField("Contents")
    rewards = StringField("Rewards")
    timelimit = StringField("Time Limit (in days)")
    submit = SubmitField("Post New Request")

class newThread(FlaskForm):
    title = StringField("Thread Title")
    contents = StringField("Contents")
    submit = SubmitField("Submit")

class newChat(FlaskForm):
    dstUser = StringField("Destination User ID")
    contents = StringField("Contents")
    submit = SubmitField("Submit")
