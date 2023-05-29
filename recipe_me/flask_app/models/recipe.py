from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import like

class Recipe:
    db = "recipes_users"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.like_count = data['like_count']
        self.liked =  None

    @classmethod #get one
    def get_recipe(cls,data):
        query = """
                SELECT *, user1.first_name as posted_by, users2.first_name as liked_by FROM recipes
                LEFT JOIN users user1 ON recipes.user_id = user1.id
                LEFT JOIN (SELECT likes.recipe_id, COUNT(1) like_count
                FROM Likes GROUP BY likes.recipe_id) 
                AS like_count ON recipe_id = recipes.id
                left join likes on likes.recipe_id = recipes.id
                left join users users2 on likes.user_id = users2.id
                left join likes as liked on recipes.id = likes.recipe_id
                AND likes.user_id = %(id)s
                """
                # """
                # SELECT * FROM recipes
                # LEFT JOIN users ON users.id = user_id
                # LEFT JOIN likes ON recipes.id = recipe_id
                # LEFT JOIN (SELECT first_name AS l_name FROM users) AS l_names
                # ON likes.user_id = users.id
                # WHERE recipes.id = %(id)s
                # """
        results = connectToMySQL(cls.db).query_db(query,data)
        
        liked_count = 0
        for row in results:
            if row['liked_by']:
                liked_count +=1
        results = results[0]
        this_recipe = cls(results)
        this_recipe.like_count = liked_count
        return this_recipe
    
    @classmethod #get all
    def get_all(cls, data):
        query = """
                SELECT * ,
                CASE WHEN EXISTS( 
                SELECT * FROM likes
                WHERE recipes.id = likes.recipe_id
                AND likes.user_id = %(id)s)
                THEN TRUE ELSE FALSE END AS liked
                FROM recipes
                LEFT JOIN users ON recipes.user_id = users.id
                LEFT JOIN (SELECT likes.recipe_id, COUNT(1) like_count  
                FROM Likes GROUP BY likes.recipe_id) 
                AS like_count ON recipe_id = recipes.id
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        all_recipes = []
        for row in results:
            this_recipe = cls(row)
            all_recipes.append(this_recipe)
        return all_recipes
    
    @classmethod #create
    def create_recipe(cls, data):
        query = """
                INSERT INTO recipes (name, description, instruction, date_cooked, under_30, user_id)
                VALUES (%(name)s, %(description)s, %(instruction)s, %(date_cooked)s, %(under_30)s, %(user_id)s)
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod #update
    def update_recipe(cls, data):
        query = """
                UPDATE recipes
                SET name = %(name)s, 
                description = %(description)s, 
                instruction = %(instruction)s, 
                date_cooked = %(date_cooked)s, 
                under_30 = %(under_30)s
                WHERE id = %(id)s
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod #delete
    def remove_recipe(cls, data):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s
                """
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def recipe_verify(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Name must be at least 3 characters long','recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description must be at least 3 characters long','recipe')
            is_valid = False
        if len(recipe['instruction']) < 3:
            flash('Instructions must be at least 3 characters long','recipe')
            is_valid = False
        if not recipe['date_cooked']:
            flash('Must enter a date!')
            is_valid = False
        if not -1< int(recipe['under_30'])<2:
            flash('Must select the amount of time it takes!', 'recipe')
            is_valid = False
        return is_valid