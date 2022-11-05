from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name   = data['first_name']
        self.last_name    = data['last_name']
        self.email        = data['email']
        self.password     = data['password']
        self.created_at  = data['created_at']

        
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL('rideshare_schema').query_db(query)
        users = []
        for i in results:
            users.append(cls(i))
        return users

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL('rideshare_schema').query_db(query,data)
        return cls(results[0])

    @classmethod
    def register(cls,data):
        query = '''INSERT INTO users
        (first_name, last_name, email, password, created_at) 
        VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s,NOW());
            '''
        return connectToMySQL('rideshare_schema').query_db(query,data)


    @classmethod
    def update(cls,data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'
        return connectToMySQL('rideshare_schema').query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE from users WHERE id = %(id)s;"
        return connectToMySQL('rideshare_schema').query_db(query,data)

    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("rideshare_schema").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(user):
        is_valid = True # we assume this is true
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("rideshare_schema").query_db(query,user)
        if len(result) >= 1:
            flash('Email already exists')
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False
        if not (user['password'] == user['confirm_password']):
            flash("Passwords don't match")
        return is_valid
