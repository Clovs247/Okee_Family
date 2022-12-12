import bcrypt
from flask_app import app
from flask_app.models import user
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt(app)

@app.route('/login/form/')
def legin_form():
    if "user_id" not in session:
        return render_template("login.html")
    else:
        return redirect('/dashboard')

@app.route('/login/', methods = ['post'])
def login():
    data = {
        'email': request.form['email']
    }
    id = user.User.get_user_by_email(data)
    if not id:
        flash("That email isn't in our database yet. Please Register")
        return redirect('/login/form/')
    else:
        session['user_id'] = id.id
        return redirect('/dashboard/')

@app.route("/register/form/")
def register_form():
    if 'user_id' not in session:
        return render_template('register.html')
    else:
        return redirect('/dashboard/')

@app.route('/register/', methods=['post'])
def register():
    is_valid = user.User.validate_user(request.form)
    if not is_valid:
        return redirect('/register/form/')
    else:
        new_user = {
            'username' : request.form['username'],
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        id = user.User.create_user(new_user)
        if not id:
            flash('Soemthing Went Wrong, Please Contact David')
            return redirect('/register/form/')
        else:
            session["user_id"] = id
            return redirect('/dashboard/')

