from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user, gear


@app.route('/all_gear/')
def display_gear():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id': session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        all_gear = gear.Gear.get_all_gear()
        return render_template('all_gear.html', logged_in_user = logged_in_user, all_gear = all_gear)
    
@app.route('/create/gear/')
def create_gear():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id': session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('create_gear.html', logged_in_user=logged_in_user)
    
@app.route('/create/gear/form/', methods=['post'])
def form_gear():
    gear_data={
        'name': request.form['name'], 
        'quantity': request.form['quantity'], 
        'description': request.form['description'], 
        'user_id': session['user_id']
    }
    is_valid=gear.Gear.validate_gear(gear_data)
    if not is_valid:
        flash('Please enter in Valid Info.')
        return redirect('/create/gear/')
    else:
        # print("########################", gear_data)
        gear.Gear.create_gear(gear_data)
        return redirect('/all_gear/')
    
@app.route('/gear/<int:gear_id>/view/')
def view_gear(gear_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id': session['user_id']
        }
        gear_data={
            'id':gear_id
        }
        logged_in_user=user.User.get_user_by_id(data)
        tool = gear.Gear.get_gear_with_user(gear_data)
        # print("############################", tool)
        return render_template('view_gear.html', logged_in_user=logged_in_user, tool=tool)
    
@app.route('/gear/<int:gear_id>/delete/')
def delete_gear(gear_id):
    gear_data={
        'id':gear_id
    }
    gear.Gear.delete_gear(gear_data)
    return redirect('/all_gear/')