from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app
from flask_app.models import users
from flask_app.models import rides
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.user_id = data['user_id']
        self.ride_id = data['ride_id']
        self.user = None


    @classmethod
    def write_message(cls,data):
        query = '''
        INSERT INTO messages
        (message, user_id,ride_id) 
        VALUES (%(message)s, %(user_id)s, %(ride_id)s) 
            '''
        return connectToMySQL('rideshare_schema').query_db(query,data)

        
    # @classmethod
    # def get_messages(cls,data):
    #     query = '''
    #     SELECT * FROM messages 
    #     LEFT JOIN rides ON messages.ride_id = rides.id
    #     LEFT JOIN users as usr ON rides.driver_id = usr.id
    #     LEFT JOIN users as ussr ON rides.rider_id = ussr.id
    #     WHERE ride_id = %(id)s
    #     '''
    #     results = connectToMySQL('rideshare_schema').query_db(query,data)
    #     result = results[0]
    #     message = cls(result)
    #     message.user = users.User(
    #         {
    #         'id':result['usr.id'],
    #         'first_name':result['first_name'],
    #         'last_name': result['last_name'],
    #         'email': result['email'],
    #         'password': result['password'],
    #         'created_at': result['created_at']
    #         }
    #         )
    #     message.driver = users.User(
    #         {
    #         'id':result['ussr.id'],
    #         'first_name':result['ussr.first_name'],
    #         'last_name': result['ussr.last_name'],
    #         'email': result['ussr.email'],
    #         'password': result['ussr.password'],
    #         'created_at': result['ussr.created_at']
    #         }
    #         )
    #     return message


# ===========================

    # @classmethod
    # def get_messages(cls):
    #     query = '''
    #     SELECT * FROM messages 
    #     LEFT JOIN rides ON messages.ride_id = rides.id
    #     LEFT JOIN users as usr ON rides.driver_id = usr.id
    #     LEFT JOIN users as ussr ON rides.rider_id = ussr.id

    #     '''
    #     results = connectToMySQL('rideshare_schema').query_db(query)
    #     messages = []
    #     for data in results:
    #         one_message = cls(data)
    #         rider_info = {
    #                         'id':data['usr.id'],
    #                         'first_name':data['first_name'],
    #                         'last_name': data['last_name'],
    #                         'email': data['email'],
    #                         'password': data['password'],
    #                         'created_at': data['created_at']
    #                         }
    #         driver_info = {
    #                         'id':data['ussr.id'],
    #                         'first_name':data['ussr.first_name'],
    #                         'last_name': data['ussr.last_name'],
    #                         'email': data['ussr.email'],
    #                         'password': data['ussr.password'],
    #                         'created_at': data['ussr.created_at']
    #                         }
    #         one_message.driver = users.User(driver_info)
    #         one_message.user = users.User(rider_info)
    #         messages.append(one_message)
    #     return messages