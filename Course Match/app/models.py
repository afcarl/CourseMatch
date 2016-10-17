import ldap
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from app import db, app

student_assosiate_table = db.Table('student_assosiate_table',
    db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
    db.Column('class_id', db.Integer, db.ForeignKey("class.id")))

teacher_assosiate_table = db.Table('teacher_assosiate_table',
    db.Column('teacher_id', db.Integer, db.ForeignKey("teacher.id")),
    db.Column('class_id', db.Integer, db.ForeignKey("class.id")))

def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    course_id = db.Column(db.String(10), index=True)
    teacher = db.Column(db.String(20), index=True)
    rating = db.Column(db.Integer)  

    def __init__(self, name, course_id, teacher):
        self.name = name
        self.course_id = course_id
        self.teacher = teacher

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), index=True, unique=True)
    username = db.Column(db.String(20), index = True)
    class_taking = db.relationship("Class",
                                    secondary = student_assosiate_table,
                                    primaryjoin=(student_assosiate_table.c.user_id == id),
                                    secondaryjoin=(student_assosiate_table.c.class_id == Class.id),
                                    backref = db.backref('student_assosiate_table', lazy="dynamic"),
                                    lazy="dynamic")     

    def __init__(self, email, username):
        self.email = email
        self.username= username
 
    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s(
            'uid=%s,ou=students,ou=people,dc=earlham,dc=edu' % username,
            password
        )
    
    def takes(self, course):
        if not self.is_taking(course):
            self.class_taking.append(course)
            return self

    def drops(self, course):
        if self.is_taking(course):
            self.class_taking.remove(course)
            return self

    def is_taking(self, course):
        return self.class_taking.filter(student_assosiate_table.c.class_id == course.id).count() > 0

    def get_class_taking(self):
        return Class.query.join(student_assosiate_table, (student_assosiate_table.c.class_id == Class.id)).filter(student_assosiate_table.c.user_id == self.id).order_by(Class.course_id.desc())

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
 
    @property
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    class_teaching = db.relationship("Class",
                                    secondary = teacher_assosiate_table,
                                    primaryjoin=(teacher_assosiate_table.c.teacher_id == id),
                                    secondaryjoin=(teacher_assosiate_table.c.class_id == Class.id),
                                    backref = db.backref('teacher_assosiate_table', lazy="dynamic"),
                                    lazy="dynamic")  
    rating = db.Column(db.Integer)  
    
    def teaches(self, course):
        if not self.is_teaching(course):
            self.class_teaching.append(course)
            return self

    def is_teaching(self, course):
        return self.class_teaching.filter(teacher_assosiate_table.c.class_id == course.id).count() > 0

    def __init__(self, name, rating=None):
        self.name = name

    def get_class_teaching(self):
        return Class.query.join(teacher_assosiate_table, (teacher_assosiate_table.c.class_id == Class.id)).filter(teacher_assosiate_table.c.teacher_id == self.id).order_by(Class.course_id.desc())


class LoginForm(Form):
    username = TextField('inputEmail', [InputRequired()])
    password = PasswordField('inputPassword', [InputRequired()])

class SearchForm(Form):
    search = TextField('search', [InputRequired()])