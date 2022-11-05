from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.users import User
from flask_app.models.rides import Ride
from flask_app.models.messages import Message
from flask_bcrypt import Bcrypt
from flask_app.controllers import userController

@app.route('/request/ride')
def request_page():
    if not session:
        return redirect('/')
    data = {'id': session['user_id']}
    return render_template('request.html', user = User.get_one(data))


@app.route('/create/ride', methods = ['POST'])
def create_ride():
    if not Ride.validate_request(request.form):
        session['destination'] = request.form['destination']
        session['pick_up'] = request.form['pick_up']
        session['details'] = request.form['details']
        return redirect('/request/ride')
    data = {
        'rider_id': request.form['rider_id'],
        'destination': request.form['destination'],
        'pick_up':request.form['pick_up'],
        'created_at':request.form['created_at'],
        'details':request.form['details']
    }
    Ride.create_ride_request(data)
    return redirect ('/dashboard')


@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id':id
    }
    Ride.delete_ride(data)
    return redirect('/dashboard')

@app.route('/update/ride/<int:ride_id>')
def add_driver(ride_id):
    data = {
        'id': ride_id,
        'driver_id': session['user_id'],
    }

    Ride.update_ride_request(data)
    Ride.all_ride_with_users()
    return redirect('/dashboard')


@app.route('/remove/driver/<int:ride_id>')
def remove_rider(ride_id):
    data = {
        'id': ride_id
    }
    Ride.remove_driver(data)
    return redirect('/dashboard')


@app.route('/details/<int:ride_id>')
def details (ride_id):
    if not session:
        return redirect('/')
    data = {
        'id':ride_id
    }
    one_ride = Ride.get_one_ride(data)
    return render_template('oneride.html', one_ride = one_ride)


@app.route('/edit/route/<int:ride_id>')
def edit_html(ride_id):
    data= {
    'id': ride_id
    }
    ride =  Ride.get_one_ride(data)
    return render_template('edit.html', ride = ride)


@app.route('/update/info', methods = ['POST'])
def udpate_info():
    if not Ride.validate_edit_request(request.form):
        return redirect (f'/edit/route/{request.form["id"]}')
    data = {
        'id': request.form['id'],
        'pick_up': request.form['pick_up'],
        'details': request.form['details']
    }
    Ride.update_location(data)
    return redirect('/dashboard')


@app.route('/message', methods = ['POST'])
def message ():
    data = {
        'user_id': session['user_id'],
        'ride_id': request.form['ride_id'],
        'message': request.form['message']
    }
    Message.write_message(data)
    return redirect (f'/details/{request.form["ride_id"]}')


