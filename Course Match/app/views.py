import os
import ldap
from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g, abort
from flask.ext.login import current_user, login_user, \
    logout_user, login_required
from app import login_manager, db, app
from app.models import User, Class, Teacher, LoginForm, SearchForm

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def get_current_user():
    g.user = current_user

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    page = 'index'
    if current_user.is_authenticated:
        signed = True
        return redirect(url_for('profile', username=current_user.username))
    else:
        signed = False
        return render_template('index.html', page=page, signed = signed)

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    signed = False
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index', page='index'))
 
    form = LoginForm(request.form)
 
    if request.method == 'POST':
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        
        try:
            User.try_login(email, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            page = 'index'
            return redirect(url_for('signin', page="signin", signed = signed))
        signed = True
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email, email)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('profile', username=user.username))
 
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('signin.html', page='signin', signed = signed)

@app.route("/profile/<username>", methods = ['GET', 'POST'])
@login_required
def profile(username):
    if request.method == "POST":
        search = SearchForm(request.form)
        text = request.form.get('search')
        return redirect(url_for("search", type="all", text=text))
    user = User.query.filter_by(username=username).first()
    if user != None:
        class_taking = user.get_class_taking()
        return render_template('profile.html', page='signin', signed=True, user=user, class_taking=class_taking)
    else:
        abort(404)

@app.route("/classes/<course_id>/<teacher>", methods = ['GET', 'POST'])
@login_required
def classes(course_id, teacher):
    if request.method == "POST":
        search = SearchForm(request.form)
        text = request.form.get('search')
        return redirect(url_for("search", type="all", text=text))
    course = Class.query.filter_by(course_id=course_id).filter_by(teacher=teacher).first()
    return render_template('class.html', page='signin', signed=True, course=course)

@app.route("/teachers/<teacher>", methods = ['GET', 'POST'])
@login_required
def teachers(teacher):
    if request.method == "POST":
        search = SearchForm(request.form)
        text = request.form.get('search')
        return redirect(url_for("search", type="all", text=text))
    teacher = Teacher.query.filter_by(name=teacher.strip()).first()
    class_teaching = teacher.get_class_teaching()
    return render_template('teacher.html', page='signin', signed=True, teacher=teacher, class_teaching=class_teaching)

@app.route("/search/<type>/<text>", methods = ['GET', 'POST'])
@login_required
def search(type, text):
    if request.method == "POST":
        search = SearchForm(request.form)
        text = request.form.get('search')
        return redirect(url_for("search", type="all", text=text))
    if type == "all":
        class_search = Class.query.filter(Class.name.contains(text)).all()  
        class_search = class_search + Class.query.filter(Class.course_id.contains(text)).all() 
        class_search = set(class_search)
        class_search = sorted(class_search, key=lambda class_search: class_search.course_id)

        user_search = User.query.filter(User.username.contains(text)).all()  
        user_search = user_search + User.query.filter(User.email.contains(text)).all() 
        user_search = set(user_search)
        user_search = sorted(user_search, key=lambda user_search: user_search.username)

        teacher_search = Teacher.query.filter(Teacher.name.contains(text)).all()  
        #teacher_search = teacher_search + Teacher.query.filter(Teacher.email.contains(text)).all() 
        #teacher_search = set(teacher_search)
        #teacher_search = sorted(teacher_search, key=lambda teacher_search: teacher_search.name)

        return render_template('search.html', page='signin', signed=True, type=type, search_result=[class_search, user_search, teacher_search])

    if type == "class":
        class_search = Class.query.filter(Class.name.contains(text)).all()  
        class_search = class_search + Class.query.filter(Class.course_id.contains(text)).all() 
        class_search = set(class_search)
        class_search = sorted(class_search, key=lambda class_search: class_search.course_id)
        return render_template('search.html', page='signin', signed=True, type=type, search_result=class_search)
    if type == "teacher":
        teacher_search = Teacher.query.filter(Teacher.name.contains(text)).all()  
        #teacher_search = teacher_search + Teacher.query.filter(Teacher.email.contains(text)).all() 
        #teacher_search = set(teacher_search)
        #teacher_search = sorted(teacher_search, key=lambda teacher_search: teacher_search.name)
        return render_template('search.html', page='signin', signed=True, type=type, search_result=teacher_search)
    if type == "user":
        user_search = User.query.filter(User.username.contains(text)).all()  
        user_search = user_search + User.query.filter(User.email.contains(text)).all() 
        user_search = set(user_search)
        user_search = sorted(user_search, key=lambda user_search: user_search.username)
        return render_template('search.html', page='signin', signed=True, type=type, search_result=user_search)

@app.route("/take_class/<course>/<teacher>")
@login_required
def take_class(course, teacher):
    course = Class.query.filter_by(name=course, teacher=teacher).first()    
    if course is None:
        flash("Class %s not found." % course)
        return redirect(url_for('index'))
    u = g.user.takes(course)
    if u is None:
        flash("Cannot take this course!")
        return redirect(url_for('index'))
    db.session.add(u)
    db.session.commit()
    flash("You are now taking " + str(course.name))
    return redirect(url_for('index'))

@app.route("/drop_class/<course>/<teacher>")
@login_required
def drop_class(course, teacher):
    course = Class.query.filter_by(name=course, teacher=teacher).first()    
    if course is None:
        flash("Class %s not found." % course)
        return redirect(url_for('index'))
    u = g.user.drops(course)
    if u is None:
        flash("Cannot drop this course!")
        return redirect(url_for('index'))
    db.session.add(u)
    db.session.commit()
    flash("You have dropped " + str(course.name))
    return redirect(url_for('index'))


@app.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('index', page = 'index', signed = False))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404