"""
Managing routes, registering and logging in
"""
###IMPORTANT: Modify pylit config to prevent seeing false negatives
from flask import redirect, url_for, render_template, flash, request
from package.forms import RegistrationForm, LoginForm, ProfileForm
from package import app, db, bcrypt, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, secure_filename
from package.models import User
from flask_login import login_user, logout_user, current_user
import os

posts = []

@app.route("/")
@app.route("/home/")
def home():
    ###template to return
    return render_template("index.html", posts=posts)

@app.route("/layout/")
def layout():
    ###template to return
    return render_template("layout.html", title="layout")


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    ##checks if form is valid, if not prints errors
    if form.validate_on_submit():

        flash(f'Account created: {form.username.data}', 'success')

        ###saves user to database
        hashedpassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, password = hashedpassword)
        db.session.add(user)
        db.session.commit()

        ###url to redirect
        return redirect(url_for("login"))
        ##tells the user their account has been created
        flash("Account created!", 'success')
        
    ###template to return    
    return render_template("register.html", form=form,title="Register")


@app.route("/login/", methods=["GET","POST"])
def login():
    form = LoginForm()

    ###if the method is POST (check if we need this later!!)
    if request.method == "POST":
        ###logs the user in
        if form.validate_on_submit:
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Check your data...")
    ###template to return        
    return render_template("login.html", form=form,title="Login")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/profile/", methods=["GET", "POST"])
def userprofile():
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    form = ProfileForm()

    ###function to update username
    def update_username(currentusername, newusername):
        ###doesn't run this if the field is blank. user shouldn't be able to submit form if so, but just in case :)
        if form.username.data:

        ###tries to update username
            try:
                value = User.query.filter_by(username=currentusername).first() ####THIS METHOD DOES NOT WORK IN CERTAIN SITUATIONS
                value.username = newusername   
                db.session.flush()
                db.session.commit()
                return redirect(url_for('userprofile')) ###FOLLOW POST/GET/REDIRECT PATTERN TO PREVENT "RESEND DATA." IF THIS IS REMOVED,
                                                ###RENDER_TEMPLATE WILL BE HIT, WHICH SENDS ANOTHER POST REQUEST. DO THIS FOR ALL PAGES THAT HAVE FORMS.
        ###if fails
            except Exception as e:
                print(f'Error in update_username {e}')
    
    ###function to update password
    def update_password(currentusername, newpassword):
        ###doesn't run this if the field is blank. user shouldn't be able to submit form if so, but just in case :)
        if form.password.data:

            ###tries to update password
            try:
                value = User.query.filter_by(username=currentusername).first()
                value.password = bcrypt.generate_password_hash(newpassword).decode('utf-8')
                db.session.flush()
                db.session.commit()
                return redirect(url_for('userprofile'))
        ###if fails
            except Exception as e:
                print(f'Error in update_password {e}')

    ###if the request method is post..
    if request.method == "POST":
        print(request.files)
        if "profileimage" in request.files:
            print("aaaa")
            file = request.files['profileimage']
            print(ALLOWED_EXTENSIONS)
            print(allowed_file(file.filename))
            if allowed_file(file.filename):
                print(User.query.filter_by(username = current_user.username).first().profile_image, "cccccccccc")
                filename = str(current_user.id) + secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                value = User.query.filter_by(username = current_user.username).first()
                value.profile_image = str(current_user.id) + filename
                db.session.flush()
                db.session.commit()
                print(User.query.filter_by(username = current_user.username).first().profile_image, "sssssssssssssssssss")
                return redirect(request.url)
            else:
                flash("Bad image")
        else:
                    ###...and the form is valid...
            if form.validate_on_submit():
                ###runs the update functions
                update_username(current_user.username, form.username.data)
                update_password(current_user.username, form.password.data)

                ###flashes a notification
                flash("Information updated.", 'success')

                ###redirects following POST/GET/REDIRECT rules
                return redirect(url_for('userprofile'))
            else:
                print(form.errors)
            
    ###template to return    
    return render_template("profile.html", form=form,title="Profile",pfp="userimages/" + User.query.filter_by(username = current_user.username).first().profile_image, uploadfolder = UPLOAD_FOLDER)
