from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    DB= 'validation_schema'

    def __init__(self, data):
        self.id= data['id']
        self.username= data['username']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(new_user):
        is_valid = True
        if len(new_user['username']) <3:
            flash('Username must be at least 3 characters long')
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']):
            flash('Please enter a valid email')
            is_valid=False
        if len(new_user['password']) <4:
            flash('Password must be 4 or more characters long')
            is_valid= False
        if new_user['password']!= new_user['confirm_password']:
            flash('Passwords did not match')
            is_valid= False
        
        return is_valid




    @classmethod
    def CreateUser(cls,data):
        query="""
        INSERT INTO users (username, email, password)
        VALUES (%(username)s, %(email)s, %(password)s)
        """

        result=connectToMySQL(cls.DB).query_db(query, data)

        return result
    
    @classmethod
    def GetUserByID(cls, data):
        query="""
        SELECT * FROM users
        WHERE id = %(user_id)s;
        """

        result=connectToMySQL(cls.DB).query_db(query, data)

        return cls(result[0])
    

    @classmethod
    def GetUserByEmail(cls, data):
        query="""
        SELECT * FROM users 
        WHERE email= %(email)s;
        """
        result=connectToMySQL(cls.DB).query_db(query, data)

        return cls(result[0])
