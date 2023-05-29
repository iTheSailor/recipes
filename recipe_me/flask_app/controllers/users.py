from flask_app import app, bcrypt
from flask_app.models import user
from flask import render_template, request, session, redirect, flash


@app.route('/')
def landing():
    
    if 'current_id' not in session:
        return render_template('index.html')
    data = {
            'id' : session["current_id"]
        }
    current_user = user.User.get_user_by_id(data)
    return render_template('index.html', user=current_user)


@app.route('/register', methods = ['POST'])
def create_user():
    if user.User.new_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : pw_hash,
        }
        user.User.register(data)
        flash("Account created!", 'welcome')
        return redirect('/')
    flash("Uh oh.. Something went wrong", 'welcome')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def log_in():
    focus = user.User.get_user_by_email(request.form)
    if not focus:
        flash("Invalid credentials: email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(focus.password, request.form['password']):
        flash("Invalid credentials", "login")
        return redirect('/')
    session['current_id'] = focus.id
    session['current_name'] = focus.first_name
    return redirect('/recipes')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




