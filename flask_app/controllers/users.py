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
    if not bcrypt.check_password_hash(id.password, request.form['password']):
        flash("Wrong Password")
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

@app.route('/profile/edit/')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id':session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('edit_profile.html', logged_in_user=logged_in_user)

@app.route('/profile/update/', methods=['post'])
def update_user():
    is_valid=user.User.validate_update(request.form)
    if not is_valid:
        return redirect('/')
    else: user_data = {
        'id' : session['user_id'],
        'username' : session['username'],
        'email' : session['email']
    }
    user.User.update_user(user_data)
    return redirect('/dashboard/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')