from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', id="btnLogin")

class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=4,max=32)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(),Length(min=4,max=32)])
    pin_code = PasswordField('PIN Code', validators=[DataRequired(),Length(min=4)])
    submit = SubmitField('Register', id="btnRegister")

class ForgetPasswordForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    pin_code = PasswordField('PIN Code', validators=[DataRequired()])
    submit = SubmitField('Reset Password', id="btnResetPwd")

class signEmotionForm(FlaskForm):
    feelings = StringField('Your Feelings (e.g. Happy/Angry)',validators=[DataRequired()])
    comments = TextAreaField('Comments')
    submit = SubmitField('Save', id="btnSubmitEmo")

class newRequestForm(FlaskForm):
    title = StringField("Request Title",validators=[DataRequired()])
    contents = TextAreaField("Contents",validators=[DataRequired()])
    rewards = IntegerField("Rewards",validators=[DataRequired(), NumberRange(min=1)])
    timelimit = IntegerField("Time Limit (in days)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Post New Request", id="btnRequest")

class newThreadForm(FlaskForm):
    title = StringField("Thread Title",validators=[DataRequired()])
    contents = TextAreaField("Contents",validators=[DataRequired()])
    submit = SubmitField("Submit", id="btnSubmitThread")

class newChatForm(FlaskForm):
    dstUser = StringField("Destination User ID",validators=[DataRequired()])
    contents = TextAreaField("Contents",validators=[DataRequired()])
    submit = SubmitField("Submit", id="btnSubmitChat")
