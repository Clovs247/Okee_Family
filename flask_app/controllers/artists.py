from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import artist_lineup, user

@app.route('/lineup/')
def display_lineup():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id':session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        lineup = artist_lineup.Artist_lineup.get_all_artists()
        return render_template('artist_lineup.html', logged_in_user=logged_in_user, lineup=lineup)
    
    
    