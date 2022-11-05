from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app
from flask_app.models import users, messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Ride:
    def __init__ (self, data):
        self.id                = data['id']
        self.destination       = data['destination']
        self.pick_up           = data['pick_up']
        self.details           = data['details']
        self.created_at        = data['created_at']
        self.rider_id          = data['rider_id']
        self.driver_id         = data['driver_id']
        self.user              = None
        self.driver            = None
        self.messages          = []


    @classmethod
    def create_ride_request(cls,data):
        query = '''
        INSERT INTO rides (destination,pick_up,details,created_at, rider_id)
        VALUES (%(destination)s, %(pick_up)s, 
        %(details)s, %(created_at)s,%(rider_id)s);
                '''
        return connectToMySQL('rideshare_schema').query_db(query,data)

    @classmethod
    def update_ride_request(cls,data):
        query = '''UPDATE rides SET 
        driver_id = %(driver_id)s WHERE id = %(id)s
                '''
        return connectToMySQL('rideshare_schema').query_db(query,data)


    @classmethod
    def delete_ride(cls,data):
        query = '''
            DELETE FROM rides WHERE id = %(id)s
                '''
        return connectToMySQL('rideshare_schema').query_db(query,data)


    @classmethod
    def remove_driver(cls,data):
        query = '''
        UPDATE rides SET driver_id = null WHERE id = %(id)s;
            '''
        return connectToMySQL('rideshare_schema').query_db(query,data)


    @classmethod
    def update_location(cls,data):
        query = '''
        UPDATE rides SET pick_up = %(pick_up)s, details = %(details)s 
        WHERE id = %(id)s;
        '''
        return connectToMySQL('rideshare_schema').query_db(query,data)



    @classmethod
    def all_ride_with_users(cls):
        query = '''
SELECT * FROM rides JOIN users 
ON rides.rider_id = users.id
JOIN users as usr ON rides.driver_id = usr.id;
                '''
        results = connectToMySQL('rideshare_schema').query_db(query)
        ride_info = []
        for data in results:
            one_ride = cls(data)
            rider_info = {
                            'id':data['users.id'],
                            'first_name':data['first_name'],
                            'last_name': data['last_name'],
                            'email': data['email'],
                            'password': data['password'],
                            'created_at': data['users.created_at']
                            }
            driver_info = {
                            'id':data['usr.id'],
                            'first_name':data['usr.first_name'],
                            'last_name': data['usr.last_name'],
                            'email': data['usr.email'],
                            'password': data['usr.password'],
                            'created_at': data['usr.created_at']
                            }
            one_ride.driver = users.User(driver_info)
            one_ride.user = users.User(rider_info)
            ride_info.append(one_ride)
        return ride_info


# WHERE driver_id = null

    @classmethod
    def rides_without_driver(cls):
        query = '''
SELECT * FROM rides JOIN users 
ON rides.rider_id = users.id
WHERE rides.driver_id IS NULL
                '''
        results = connectToMySQL('rideshare_schema').query_db(query)
        ride_info = []
        for data in results:
            one_ride = cls(data)
            rider_info = {
                            'id':data['users.id'],
                            'first_name':data['first_name'],
                            'last_name': data['last_name'],
                            'email': data['email'],
                            'password': data['password'],
                            'created_at': data['users.created_at']
                            }
            # driver_info = {
            #                 'id':data['usr.id'],
            #                 'first_name':data['usr.first_name'],
            #                 'last_name': data['usr.last_name'],
            #                 'email': data['usr.email'],
            #                 'password': data['usr.password'],
            #                 'created_at': data['usr.created_at']
            #                 }
            # one_ride.driver = users.User(driver_info)
            one_ride.user = users.User(rider_info)
            ride_info.append(one_ride)
        return ride_info
        

    @classmethod
    def get_one_ride(cls,data):
        query = '''
         SELECT * FROM rides 
        LEFT JOIN users as driver ON rides.driver_id = driver.id
        LEFT JOIN users as rider ON rides.rider_id = rider.id
        LEFT JOIN messages ON messages.ride_id = rides.id
        LEFT JOIN users ON messages.user_id = users.id
        WHERE rides.id = %(id)s
                '''
        results = connectToMySQL('rideshare_schema').query_db(query,data)
        result = results[0]
        ride = cls(result)
        ride.user = users.User(
            {
            'id':result['rider.id'],
            'first_name':result['rider.first_name'],
            'last_name': result['rider.last_name'],
            'email': result['rider.email'],
            'password': result['rider.password'],
            'created_at': result['rider.created_at']
            }
            )
        ride.driver = users.User(
            {
            'id':result['driver.id'],
            'first_name':result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['created_at']
            }
            )
        for row  in results:
            message = {
            'id':row['messages.id'],
            'message':row['message'],
            'user_id': row['user_id'],
            'ride_id': row['ride_id'],
            'created_at': row['driver.created_at']
            }
        
            one_message = messages.Message(message)
            one_message.user = users.User(
            {
            'id':row['users.id'],
            'first_name':row['users.first_name'],
            'last_name': row['users.last_name'],
            'email': row['users.email'],
            'password': row['users.password'],
            'created_at': row['users.created_at']
            }
            )
            ride.messages.append(one_message)
        return ride

    @staticmethod
    def validate_request (ride):
        is_valid = True
        if len(ride['destination']) < 3:
            flash('Destination must be 3 characters long')
            is_valid = False
        if len(ride['pick_up']) < 3:
            flash('Pick up location must be 3 characters long')
            is_valid = False
        if len(ride['details']) < 10:
            flash('Details must be 10 characters long ')
            is_valid = False
        if len(ride['created_at']) == 0:
            flash('Please select a date')
            is_valid = False
        return is_valid
    @staticmethod

    def validate_edit_request (ride):
        is_valid = True

        if len(ride['pick_up']) < 3:
            flash('Pick up location must be 3 characters long')
            is_valid = False
        if len(ride['details']) < 10:
            flash('Details must be 10 characters long ')
            is_valid = False

        return is_valid