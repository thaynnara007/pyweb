from flask_wtf import FlaskForm
from app.models.user import User
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', 
    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if (user is not None): raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(user is not None): raise ValidationError('Please use a different email.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('Abou me', validators=[Length(min=0, max=140)])
    submit = SubmitField()

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        if(username.data != self.original_username):
            other_user = User.query.filter_by(username=self.username.data).first()

            if(other_user is not None): return ValidationError('Please use a different username')