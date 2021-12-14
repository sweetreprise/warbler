from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing a user."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header URL')
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[DataRequired()])

# class PasswordValidationForm(FlaskForm):
#     """Checks if password is valid to edit user details"""

#     password = PasswordField("Password")

#     def __init__(self, user, *args, **kwargs):
#         super(PasswordValidationForm, self).__init__(*args, **kwargs)
#         self.user = user
        
#     def validate_password(self, field):
#         if field.data != self.user.password:
#             raise ValidationError("Your password is incorrect.")
