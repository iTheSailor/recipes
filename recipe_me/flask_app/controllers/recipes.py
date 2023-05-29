from flask_app import app
from flask_app.models import recipe, like
from flask import session, render_template, redirect, request, flash

@app.route('/recipes')
def dashboard():
    if len(session)== 0:
        flash('You must be signed in to view this page', 'reg')
        return redirect('/')
    data = {
        'id' : session['current_id']
    }
    everything = recipe.Recipe.get_all(data)
    return render_template("dashboard.html", all_recipes = everything, user = session)

@app.route('/recipes/new')
def recipe_form():
    return render_template("new_recipe.html", user=session)

@app.route('/recipes/add', methods=['POST'])
def add_new_recipe():
    print(request.form)
    if not recipe.Recipe.recipe_verify(request.form):
        return redirect('/recipes/new')
    recipe.Recipe.create_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/edit/<int:id>')
def edit_recipe_route(id):
    data = {
        'id' : id
    }
    focus = recipe.Recipe.get_recipe(data)
    if session['current_id'] != focus['user_id']:
        flash('not authorized' , 'warning')
        return redirect('/recipes')
    return render_template("edit_recipe.html", recipe = focus)

@app.route('/recipes/edit_confirm', methods=['POST'])
def edit_recipe():
    recipe.Recipe.update_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/show/<id>')
def show_recipe(id):
    data ={
        'id' : id
    }
    focus = recipe.Recipe.get_recipe(data)
    
    return render_template('recipe.html', user=session, recipe=focus)


@app.route('/recipes/delete/<id>')
def delete_recipe(id):
    data={
        'id' : id
    }
    author = recipe.Recipe.get_recipe(data)
    if session['current_id'] == author['user_id']:
        recipe.Recipe.remove_recipe(data)
        return redirect('/recipes')
    else:
        flash('not authorized' , 'warning')
        return redirect('/recipes')
    
@app.route("/recipes/like/<id>", methods = ['post'])
def like_recipe(id):
    data ={
        'recipe_id': id,
        'user_id' : session['current_id']
    }
    like.Like.like_recipe(data)
    return redirect('/recipes')

@app.route("/recipes/unlike/<id>", methods = ['post'])
def unlike_recipe(id):
    data ={
        'recipe_id': id,
        'user_id' : session['current_id']
    }
    like.Like.undo_like(data)
    return redirect('/recipes')
