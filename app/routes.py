from flask import render_template, flash, redirect, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user

from app import app 
from app import db
from app.forms import SignInForm, SignUpForm
from app.models import User, Promotion


##
# INDEX / LOGIN ROUTE
##
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignInForm()

    #IF USER CONNECTED REDIRECT TO DASHBOARD
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    #SEND FROM IF CONDITIONS = OK AND REDIRECTS
    if request.method == 'POST' and form.validate_on_submit():

        #VERIFY IF USER EXIST IN DATABASE
        user = User.query.filter_by(username=form.username.data).first()
        
        #IF USER OR PASSWORD DONT MATCH RETURN TO LOGIN
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('dashboard'))
    
    return render_template('signin.html', title='Sign In', form=form)


    #     session.permanent = True
    #     user = request.form
    #     session["user"] = user
    #     flash('Bienvenue à vous {}, remember_me={}'.format(form.username.data, form.remember_me.data, "info"))
    #     return redirect(url_for('dashboard'))

    #     found_user = users.query.filter_by(name = user).first()
    #     if found_user:
    #         session["email"] = found_user.email
    #     else:
    #         usr = users(user, "")
    #         db.session.add(usr)
    #         db.session.commit()

    # else:
    #     if "user" in session: 
    #         return redirect(url_for('dashboard'))
        
   

##
# SIGNUP ROUTE
##
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    form.promo_choice.choices = [(promotion.id_promotion, promotion.code) for promotion in Promotion.query.all()]

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        flash(f"Vous êtes déja inscrit sur notre application !", "info")

    #Send form if conditions = OK and redirect
    if request.method == 'POST' and form.validate_on_submit():
        user = User(lastname = form.lastname.data, firstname = form.firstname.data, username=form.username.data, email=form.email.data, birthday=form.birthday.data)
        user.set_password(form.password.data)
        promotion = Promotion.query.filter_by(id_promotion = form.promo_choice.data).first()
                    
        db.session.add(user)
        promotion.promotions.append(user)
        db.session.commit()
        flash('Votre inscription a été prit en compte {}. Veuillez vérifier vos email pour confirmer votre inscription'.format(form.username.data, "info"))
        return redirect(url_for('index'))
    
    return render_template('signup.html', title='Sign Up', form=form)    

##
# LOGOUT ROUTE
##
@app.route('/logout')
def logOut():
    logout_user()
    flash(f"Vous avez été déconnecté de l'application !", "info")
    return redirect(url_for('index'))

##
# DASHBOARD ROUTE
##
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        #Return template index.html with data
        return render_template('dashboard.html', title='Dashboard')
    
    else:
        #Redirect to signin route
        return redirect(url_for("index"))

##
# PROFIL ROUTE
##
@app.route('/profil')
@login_required
def profil():
        if request.method == "POST" and form.validate_on_submit():
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]

        #Return template index.html with data
        return render_template('profil.html', title='Profil')


##
# ADMIN_DASHBOARD ROUTE
## 
@app.route('/administration/dashboard')
@login_required
def a_dashboard():
        user = current_user


        return render_template('administration/dashboard.html', title='Administration', user=user)