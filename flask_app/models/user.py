from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db='okee_family'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.car = []
        # self.gear = []


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO user
        (username, email, password)
        VALUES
        (%(username)s, %(email)s, %(password)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Read &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * FROM user
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        members = []
        for row in results:
            members.append(cls(row))
        return members

    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM user
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM user
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Update &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def update_user(cls, data):
        query = """
        UPDATE user SET
        username = %(username)s,
        email = %(email)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Delete &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def delete_user(cls, data):
        query = """
        DELETE FROM user
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Validate &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = """
        SELECT * FROM user
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            is_valid = False
            flash("That Email has already been entered into the database")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Format")
        if len(user['username'])<1:
            is_valid = False
            flash("Username must contain at least 1 character")
        if len(user['username'])>15:
            is_valid = False
            flash("Username must not contain more than 15 characters")
        if len(user['password'])<8:
            is_valid = False
            flash("Password must contain at least 8 characters")
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Password are not matching, double check your spelling.")
        return is_valid

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Connection &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

