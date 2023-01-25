from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        all_users = user.User.get_all_users()
        return render_template('dashboard.html', logged_in_user=logged_in_user)

@app.route('/lineup-full/')
def lineup_full():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('lineup.html', logged_in_user=logged_in_user)

@app.route('/lineup-map/')
def lineup_map():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('lineup_map.html', logged_in_user=logged_in_user)

@app.route('/lineup-stages/')
def lineup_stages():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('stage_lineup.html', logged_in_user=logged_in_user)

@app.route('/campground/')
def campground():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('campgrounds.html', logged_in_user=logged_in_user)

@app.route('/playlist/')
def playlist():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('playlists.html', logged_in_user=logged_in_user)

@app.route('/rules/')
def rules():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id':session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('rules.html', logged_in_user=logged_in_user)

@app.route('/prohibited-items/')
def prohibited_items():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id':session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('prohibited_items.html', logged_in_user=logged_in_user)

@app.route('/food/')
def food():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id':session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('food.html', logged_in_user=logged_in_user)

