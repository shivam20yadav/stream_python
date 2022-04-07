from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from web.models import User
from flask import Blueprint,render_template
from flask import request
from flask_login import current_user

views = Blueprint('views',__name__)


@views.route('/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(user_name=username).first()
    if user:
        if user.password == password:
            #flash('se, try again.', category='error')
            return redirect(url_for('auth.home'))
        else:
            flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')

    return render_template("login.html",user=current_user)

