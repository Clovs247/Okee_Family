from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Artist_lineup:
    db='okee_family'
    def __init__(self, data):
        self.id = data['id']
        self.artist_name = data['artist_name']
        self.stage_name = data['stage_name']
        self.set_time = data['set_time']
        self.total_likes = 0


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Create &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def create_artist(cls, data):
        query = """
        INSERT INTO artist_lineup
        (artist_name, set_time)
        VALUES
        (%(artist_name)s, %(set_time)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print(data)
        return results
    
    @classmethod
    def like_artist(cls, data):
        query="""
        INSERT INTO like
        (user_id, artist_id)
        VALUES
        (%(user_id)s, %(artist_id)s)
        """
        print(data)
        return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Read &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    @classmethod
    def get_all_artists(cls):
        query="""
        SELECT * FROM artist_lineup
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_artist_by_id(cls, data):
        query="""
        SELECT * FROM artist_lineup
        WHERE id = %(id)s
        ;"""
        results =connectToMySQL(cls.db).query_db(query, data)
        if len(results)>1:
            return False
        else:
            return results

    @classmethod
    def get_artist_likes_by_user(cls, data):
        query="""
        SELECT * FROM like
        LEFT JOIN user
        ON like.user_id = user.id
        LEFT JOIN artist_lineup
        ON like.artist_id = artist_lineup.id
        WHERE user.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        # print("##########################", results)
        if len(results)<1:
            return False
        return cls(results[0])

    # @classmethod
    # def get_gear_by_user(cls, data):
    #     query="""
    #     SELECT * FROM gear
    #     LEFT JOIN user
    #     ON gear.owner = user.id
    #     WHERE gear.owner = %(id)s
    #     ;"""
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     # print("##########################", results)
    #     return results


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Update &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # @classmethod
    # def update_gear(cls, data):
    #     query="""
    #     UPDATE gear SET
    #     name = %(name)s
    #     quantity = %(quantity)s
    #     description = %(description)s
    #     WHERE id = %(id)s
    #     ;"""
    #     return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Delete &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # @classmethod
    # def delete_gear(cls, data):
    #     query = """
    #     DELETE FROM gear
    #     WHERE id = %(id)s
    #     ;"""
    #     return connectToMySQL(cls.db).query_db(query, data)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Validation &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&