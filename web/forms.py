from flask_wtf import FlaskForm as BaseForm
from wtforms.fields import StringField, SubmitField
#from wtforms.validators import Required


class LoginForm(BaseForm):
    """Accepts a nickname and a room."""
    name = StringField('Name', render_kw={'style':'border-radius: 4px;  width:300px; padding-left: 10px; height:30px'})
    room = StringField('Room', render_kw={'style':'border-radius: 4px;  width:300px; padding-left: 10px; height:30px'})
    submit = SubmitField('Enter Chatroom',render_kw={'style':'border-radius: 4px;  width:300px; padding-left: 10px; height:30px;margin-left:45px'})
