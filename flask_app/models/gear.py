from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Gear:
    db='okee_family'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.quantity = data['quantity']
        self.description = data['description']
        self.owner = data['owner']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def create_gear(cls, data):
        query = """
        INSERT INTO gear
        (name, quantity, description, owner)
        VALUES
        (%(name)s, %(quantity)s, %(description)s, %(user_id)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print(data)
        return results

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Read &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def get_all_gear(cls):
        query="""
        SELECT * FROM gear
        LEFT JOIN user
        ON gear.owner =user.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_gear_by_id(cls, data):
        query="""
        SELECT * FROM gear
        WHERE id = %(id)s
        ;"""
        results =connectToMySQL(cls.db).query_db(query, data)
        if len(results)>1:
            return False
        else:
            return results

    @classmethod
    def get_gear_with_user(cls, data):
        query="""
        SELECT * FROM gear
        LEFT JOIN user
        ON gear.owner = user.id
        WHERE gear.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print("##########################", results)
        return results


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Update &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def update_gear(cls, data):
        query="""
        UPDATE gear SET
        name = %(name)s
        quantity = %(quantity)s
        description = %(description)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Delete &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def delete_gear(cls, data):
        query = """
        DELETE FROM gear
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Validation &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @staticmethod
    def validate_gear(gear_data):
        is_valid= True
        query="""
        SELECT * FROM gear
        WHERE name = %(name)s
        ;"""
        results = connectToMySQL(Gear.db).query_db(query, gear_data)
        print("***************VALIDATE*************",gear_data)
        if len(gear_data['name'])<2:
            is_valid= False
            flash("Please enter in a name that is easily identifable.")
        if int(gear_data['quantity']) <0:
            is_valid=False
            flash("Please bring the item rather than just listing it.")
        return is_valid