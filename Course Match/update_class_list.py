from app import db, app
from app.models import Class, Teacher
import pickle, sys

commit = False
if sys.argv[1] == "new":
    fopen = pickle.load(open("Data\Courses_data.p", "rb"))
    for data in fopen:
        course = Class(data[0].strip(), data[1].strip(), data[2].strip())
        teacher = Teacher(data[2].strip())
        db.session.add(course)
        db.session.add(teacher)
    db.session.commit()

elif sys.argv[1] == "add":
    fopen = pickle.load(open("Data\Courses_data.p", "rb"))
    for data in fopen:
        course = Class.query.filter_by(name=data[0].strip(), teacher=data[2].strip()).first()
        if not course:
            course = Class(data[0].strip(), data[1].strip(), data[2].strip())
            db.session.add(course)
            commit = True
        for name in data[2].split(","):
            teacher = Teacher.query.filter_by(name=name.strip()).first()
            if not teacher:
                teacher = Teacher(name.strip())
                db.session.add(teacher)
                commit = True
    if commit == True:
        db.session.commit()
    #Add relation between teachers and classes they are teaching
    for data in fopen:
        course = Class.query.filter_by(name=data[0].strip(), teacher=data[2].strip()).first()
        for name in data[2].split(","):
            teacher = Teacher.query.filter_by(name=name.strip()).first()
            teacher.teaches(course)
            db.session.add(teacher)
    db.session.commit()
