from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Car:
    db = 'okee_family'
    def __init__(self, data):
        self.id = data['id']
        self.car_name = data['car_name']
        self.car_capacity = data['car_capacity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.passengers = []
        
        
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def create_car(cls, data):
        query="""
        INSERT INTO car
        (car_name, car_capacity)
        VALUES
        (%(car_name)s, %(car_capacity)s)
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
            car_now.passengers = cls.get_voyagers(car_data)
            voyagers.append(car_now)
            return cls(results[0])
    
    @classmethod
    def get_car_by_driver(cls, data):
        pass
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Update &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
