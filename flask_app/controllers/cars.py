from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user, car


@app.route('/all_cars/')
def display_cars():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        all_cars = car.Car.get_all_cars()
        for results in all_cars:
            print(results.car_name)
        return render_template('all_cars.html', logged_in_user = logged_in_user, all_cars = all_cars)
    
@app.route('/create/car/')
def create_car_page():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'id' : session['user_id']
        }
        logged_in_user = user.User.get_user_by_id(data)
        return render_template('create_car.html', logged_in_user = logged_in_user)
    
@app.route('/create/car/form/', methods = ['post'])
def form_car():
    car_data = {
        'car_name': request.form['car_name'],
        'car_capacity': request.form['car_capacity'],
        'user_id': session['user_id']
    }
    is_valid = car.Car.validate_car(car_data)
    if not is_valid:
        flash('Please enter in valid info.')
        return redirect('/')
    else:
        print("***********CREATE CAR FORM***************", car_data)
        car.Car.create_car(car_data)
        return redirect('/all_cars/')
    
@app.route('/join/<int:car_id>/form/', methods = ['post'])
def join_car(car_id):
    val_data={
        'user_id': session['user_id'],
        'car_id': car_id
    }
    is_valid= car.Car.validate_rider(val_data)
    if not is_valid:
        
        return redirect(f'/car/{car_id}/view/')
    else:
        car_data = {
            'user_id': session['user_id'],
            'car_id':car_id
        }
        car.Car.join_ride(car_data)
        return redirect('/all_cars/')
    
@app.route('/car/<int:car_id>/view/')
def view_car(car_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        car_data={
            'id': car_id
        }
        logged_in_user = user.User.get_user_by_id(data)
        vessel= car.Car.get_car_with_passengers(car_data)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$", vessel)
        return render_template('view_car.html', logged_in_user=logged_in_user, vessel=vessel)
    
@app.route("/car/<int:car_id>/delete/")
def delete_car(car_id):
    car_data={
        'id':car_id
    }
    car.Car.delete_car(car_data)
    return redirect('/all_cars/')

@app.route('/car/<int:car_id>/leave')
def leave_car(car_id):
    betrayer_data={
        'user_id' :session['user_id'],
        'car_id': car_id
    }
    print(betrayer_data)
    car.Car.leave_car(betrayer_data)
    return redirect(f'/car/{car_id}/view/')