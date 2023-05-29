from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
class User:
    db = "recipes_users"
    liked = []
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def register(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        print (results)
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return results[0]
    


    @staticmethod
    def new_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters long", "reg")
            is_valid = False
        if not NAME_REGEX.match(user['first_name']):
            flash("Can only use letters in first name", "reg")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters long", "reg")
            is_valid = False
        if not NAME_REGEX.match(user['last_name']):
            flash("Can only use letters in last name", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please use a valid email", "reg")
            is_valid = False
        if len(user['password']) < 8:
            flash("Passwords must be at least 8 characters", 'reg')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Password must include 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character", "reg")
            is_valid = False
        if not user["password"] == user["confirm_pass"]:
            flash("Passwords do not match", "reg")
            is_valid = False
        return is_valid