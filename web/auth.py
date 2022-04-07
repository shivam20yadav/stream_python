from flask_login import login_manager, login_required,current_user
from flask_login.utils import logout_user
from web.models import User
from flask import Blueprint,render_template,redirect, session,url_for, Response
from flask import request,flash
from .forms import LoginForm
from . import db
from . import events
import pyautogui
import cv2
import numpy as np
from web.models import feedback
from .view import login

auth = Blueprint('auth',__name__)

@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        user = request.form.get('username')
        pass1 = request.form.get('password')  
        new_user = User(user_name = user,password = pass1)
        db.session.add(new_user)
        db.session.commit() 
        flash('Account created!', category='success')
        return redirect(url_for('views.login'))   
    return render_template("sign-up.html")

@auth.route("/home",methods=['GET','POST'])
def home(): 
    return render_template("home1.html")

camera = cv2.VideoCapture(0)
frame_width = int(camera.get(3))
frame_height = int(camera.get(4))

size = (frame_width, frame_height)

result = cv2.VideoWriter('recording.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)
def gen_frames():
    while True:
        try:
            img = pyautogui.screenshot()
            frame1 = np.array(img)
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            grabbed, frame2 = camera.read() 
            temp = frame1
            small = cv2.resize(frame2,(220,220))
            x = 1700
            y = 825
            x_e = x + small.shape[1]
            y_e = y + small.shape[0]
            temp[y:y_e,x:x_e] = small
            ret, buffer = cv2.imencode('.jpg', temp)
            result.write(buffer)
            temp= buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + temp + b'\r\n')
        except KeyboardInterrupt:
            break

@auth.route('/stream_feed')
def stream_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@auth.route('/view_feed')
def view_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@auth.route('/suggestion', methods=['GET', 'POST'])
def with_suggestions():    
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)
@auth.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.with_suggestions'))
    return render_template('chat.html', name=name, room=room)

@auth.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        user = current_user
        user.password = request.form.get('pass2')
        db.session.commit()
        flash('Password has been updated!', 'success')
        return redirect(url_for('.home'))
    return render_template('edit.html',user=current_user)

@auth.route('/feedback',methods=['GET','POST'])
def feed():
    if request.method == 'POST':
        fnam = request.form.get('fnam')
        lnam = request.form.get('lnam') 
        mess = request.form.get('subject')  
        new = feedback(first_name=fnam,last_name=lnam,message=mess)
        db.session.add(new)
        db.session.commit() 
        flash('feedback submitted', category='success')
        return redirect(url_for('.feed'))
    return render_template('feedback.html',query=feedback.query.all())
@auth.route('/s',methods=['GET','POST'])
def stream():
    return render_template('stream.html')
@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))
@auth.route('/chat1')
def chat1():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.sugg'))
    return render_template('chat1.html', name=name, room=room)
@auth.route('/sugg', methods=['GET', 'POST'])
def sugge():    
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat1'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)
@auth.route('/v',methods=['GET','POST'])
def view():
    return render_template('view.html')