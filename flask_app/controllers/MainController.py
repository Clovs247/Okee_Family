from flask import render_template, redirect, session
from flask_app import app
from flask_app.models import user



@app.route('/')
def index():
    return "success"
    # return render_template("index.html")

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('dashboard.html', logged_in_user)
