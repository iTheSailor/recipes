from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe

class Like:
    db = "recipes_users"

    def __init__(self, data):
        self.user_id = data['user_id']
        self.recipe_id = data['recipe_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod #like
    def like_recipe(cls, data):
        query = """
                INSERT INTO likes (user_id, recipe_id)
                VALUES (%(user_id)s, %(recipe_id)s)
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod #undo like
    def undo_like(cls, data):
        query = """
                DELETE FROM likes
                WHERE user_id = %(user_id)s 
                AND recipe_id = %(recipe_id)s
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    # @classmethod #count like
    # def track_likes(cls, data):
    #     query = """
    #             SELECT recipes.id,
    #             CASE 
    #             WHEN EXISTS( 
    #             SELECT * FROM likes
    #             WHERE recipes.id = likes.recipe_id
    #             AND likes.user_id = %(id)s)
    #             THEN TRUE 
    #             ELSE FALSE END 
    #             AS liked FROM recipes
    #             """
    #     return connectToMySQL(cls.db).query_db(query,data)