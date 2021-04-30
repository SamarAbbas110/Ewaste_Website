from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileField , FileRequired
from wtforms import Form ,StringField, IntegerField , TextAreaField , SubmitField ,PasswordField , BooleanField ,validators
from wtforms.validators import Email, DataRequired , Length , EqualTo 

class LoginForm(FlaskForm):
    email = StringField('EMAIL' , validators=[DataRequired() , Length(min=5 ,max=60), Email()], render_kw={'placeholder': "Email"})
    password = PasswordField('PASSWORD' , validators=[DataRequired() , Length(min=5 ,max=60)], render_kw={'placeholder': "Password"})
    remember_me = BooleanField('remember me')
    submit = SubmitField('LOGIN')

class RegistrationForm(FlaskForm):
    first_name = StringField('firstname' , validators=[DataRequired() , Length(max=60)], render_kw={'placeholder': "First Name"})
    last_name = StringField('lastname' , validators=[DataRequired() , Length(max=60)], render_kw={'placeholder': "Last Name"})
    email = StringField('email' , validators=[DataRequired() , Length(min=5 ,max=60), Email() ], render_kw={'placeholder': "Email"})
    password = PasswordField('password' , validators=[DataRequired() , Length(min=5 ,max=60)], render_kw={'placeholder': "Password"})
    submit = SubmitField('REGISTRATION')
 
class ChangePasswordForm(FlaskForm):
    name = StringField('name' , validators=[DataRequired() , Length(min=5 ,max=60) ])
    email = StringField('email' , validators=[DataRequired() , Length(min=5 ,max=60), Email() ])
    password = PasswordField('password' , validators=[DataRequired() , Length(min=5 ,max=60)])
    remember = BooleanField('remember me')
    submit = SubmitField('SIGN IN')


class AddProductForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=5 ,max=60)], render_kw={'placeholder': "Enter Product Name"})
    category = StringField('Category',validators=[DataRequired()], render_kw={'placeholder': "Enter Category Name"})
    price  = IntegerField('Price',validators=[DataRequired()], render_kw={'placeholder': "Enter Price"})
    description = TextAreaField('Descripton',validators=[DataRequired()], render_kw={'placeholder': "Enter Description"})
    image = FileField('image' ,validators=[FileRequired(), FileAllowed(['jpg' , 'png', 'jpeg'], "Images Only!")], render_kw={'placeholder': "Choose Image"})
    submit = SubmitField('ADD Product')

class contact(FlaskForm):
    name = StringField('Name' , validators=[DataRequired() , Length(max=60)], render_kw={'placeholder': "Enter your Name"})
    email = StringField('Email' , validators=[DataRequired() , Length(max=60)], render_kw={'placeholder': "Enter ypu Email"})
    phone = IntegerField('Phone' , validators=[DataRequired() , Length(min=5 ,max=60), Email() ], render_kw={'placeholder': "Enter you phone Number"})
    message = PasswordField('Message' , validators=[DataRequired() , Length(min=5 ,max=60)], render_kw={'placeholder': "Enter the Message"})
    submit = SubmitField('CONTACT')

class DetailForm(FlaskForm):
    phone = StringField('Phone' , validators=[DataRequired() , Length(min=5 ,max=60) ], render_kw={'placeholder': "Enter you phone Number"})
    address = StringField('Address' , validators=[DataRequired() , Length(min=5 ,max=255)], render_kw={'placeholder': "Enter the Address"})
    submit = SubmitField('submit')








 