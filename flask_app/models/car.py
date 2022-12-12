from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Car:
    db = 'okee_family'
    def __init__(self, data):
        self.id = data['id']
        self.car_name = data['car_name']
        self.car_capacity = data['car_capacity']
        self.driver = data['driver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.passengers = []
        
        
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def create_car(cls, data):
        query="""
        INSERT INTO car
        (car_name, car_capacity, driver)
        VALUES
        (%(car_name)s, %(car_capacity)s, %(user_id)s)
        ;"""
        car_id = connectToMySQL(cls.db).query_db(query, data)
        data["car_id"] = car_id
        cls.join_ride(data)
        return car_id
    
    @classmethod
    def join_ride(cls, data):
        query="""
        INSERT INTO passenger
        (car_id, user_id)
        VALUES
        (%(car_id)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Read &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def get_all_cars(cls):
        query="""
        SELECT * FROM car
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        voyagers = []
        for row in results:
            car_now = cls(row)
            data = {
                'car_id' : car_now.id
            }
            car_now.passengers = cls.get_passengers(data)
            voyagers.append(car_now)
        return voyagers
    
    @classmethod
    def get_a_car(cls, data):
        query = """
        SELECT * FROM car
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        voyagers = []
        if len(results)<1:
            return False
        else:
            car_now = cls(results)
            car_data = {
                'car_id' : car_now.id
            }
            car_now.passengers = cls.get_passengers(car_data)
            voyagers.append(car_now)
            return cls(results[0])
    
    @classmethod
    def get_car_by_driver(cls, data):
        query="""
        SELECT * FROM car
        WHERE driver = %(driver)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_car_with_passengers(cls, data):
        query = """
        SELECT * FROM car
        LEFT JOIN passenger
        ON passenger.car_id = car.id
        LEFT JOIN user
        ON passenger.user_id = user.id
        WHERE team.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        vessel = cls(results[0])
        for row_from_db in results:
            user_data = {
                "id":row_from_db["user.id"],
                "username":row_from_db["user.username"],
                "email":row_from_db["user.email"],
                "created_at":row_from_db["user.created_at"],
                "updated_at":row_from_db["user.updated_at"]
            }
            rider = user.User(user_data)
            vessel.passengers.append(rider)
        return vessel
    
    @classmethod
    def get_passengers(cls, data):
        query="""
        SELECT * FROM passenger
        JOIN user
        ON passenger.user_id = user.id
        WHERE passenger.car_id = %(car_id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        voyagers = []
        for row in results:
            voyagers.append(user.User(row))
        return voyagers
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Update &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Delete &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def delete_car(cls, data):
        query = """
        DELETE FROM car
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def leave_team(cls, data):
        query="""
        DELETE FROM passenger
        WHERE user_id = %(user_id)s
        AND car_id = %(car_id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Validate &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @staticmethod
    def validate_car(car_data):
        is_valid = True
        query="""
        SELECT * FROM car
        WHERE car_name = %(car_name)s
        ;"""
        results = connectToMySQL(Car.db).query_db(query, car_data)
        if len(car_data['car_name']) <= 3:
            is_valid = False
            flash("Please name your car with at least 3 characters, so we know which car is which.")
        if car_data["car_capacity"] <=0:
            is_valid=False
            flash("Its not a ghost car, how many people fit in it?")
        if car_data["car_capacity"] >10:
            is_valid=False
            flash("ARE YOU DRIVING A BUS?!")
        return is_valid
    
    @staticmethod
    def validate_rider(rider):
        query="""
        SELECT * FROM passenger
        WHERE user_id = %(id)s
        AND car_id = %(car_id)s
        ;"""
        results = connectToMySQL(Car.db).query_db(query, rider)
        if len(results)>0:
            flash("One seat can fit One rider. Leave the extra seat to someone else.")