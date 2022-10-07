""" Modules required to handle the backend """
from flask import Flask, render_template, request

app = Flask(__name__)

# for the time being, we will hold a piece of data for development here and later delete
# and replace it with actual data from our database
# pylint: disable=line-too-long

# user information
users = {'guest': {'pw': '1234',
                   'discId': 'guest#1234',
                   'courses': [("CS225", '', ''), ("CS222", '74484', 'SL1'), ("CS233", '', ''), ("MATH415", '', ''), ("STAT400", '', '')]},
         'XXX': {'pw': '0000',
                 'discId': '',
                 'courses': [("CS374", '', ''), ("CS440", '', ''), ("CS341", '', ''), ("CS498", '', '')]},
         'YYY': {'pw': '0000',
                 'discId': '',
                 'courses': [("CS128", '', ''), ("MATH231", '', ''), ("CS173", '', '')]},
         'ZZZ': {'pw': '0000',
                 'discId': '',
                 'courses': [("CS225", '', ''), ("CS222", '74484', 'SL1'), ("CS233", '', ''), ("STAT410", '', '')]}}
# sample section information to display course information
sections = [{'year': '2022',
            'semester': 'fall',
            'subjectName': 'Computer Science',
            'subjectId': 'CS',
            'courseNum': '222',
            'courseName': 'Software Design Lab',
            'description': "Design and implementation of novel software solutions. Problem identification and definition; idea generation and evaluation; and software implementation, testing, and deployment. Emphasizes software development best practices—including framework selection, code review, documentation, appropriate library usage, project management, continuous integration and testing, and teamwork. Prerequisite: CS 128; credit or concurrent registration in CS 225. Restricted to majors in Computer Science undergraduate curricula only.",
            'creditHours': '1 hours',
            'CRN': '74484',
            'sectionNum': 'SL1',
            'sectionType': 'Lecture-Discussion',
            'startTime': '02:00 PM',
            'endTime': '02:50 PM',
            'daysOfTheWeek': 'F',
            'roomNum': '0027/1025',
            'buildingName': 'Campus Instructional Facility',
            'mainInstructor': "Woodley, M"}]

@app.route('/')
def index():
    """Route for /"""
    return render_template("index.html"), 200

@app.route('/main', methods=["POST"])
def user_login():
    """Route for /main"""
    items = request.form
    if items["netid"] in users:
        if items["pw"] == users[items["netid"]]['pw']:
            # successfully logged in
            required_info = []
            # here, we're supposed to manipulate data, writing queries and so on
            # but due to the issue where we don't have any solid idea as to
            # how to host a web/SQL server
            required_info.append(items["netid"])
            required_info.append(users[items["netid"]]['courses'])
            required_info.append(list(users.keys())[1:])
            return render_template("main.html", items=required_info), 200
    # did not successfully logged in (have to do something with this)
    return render_template("error.html"), 404

@app.route('/register', methods=["POST"])
def register():
    """Route for /register"""
    return render_template("register.html"), 200

@app.route('/user_info', methods=["POST"])
def user_info():
    """ Route for /user_info
        This is supposed to show user information but
        is under development at this moment.
    """
    return render_template("base.html"), 200

@app.route('/section/<course>/<section>', methods=["POST"])
def section_info(course, section):
    """Route for /section"""
    # look up a section info
    for sec in sections:
        course_num = sec['subjectId'] + sec['courseNum']
        if course_num == course and sec['sectionNum'] == section:
            items = sec
            return render_template("section.html", items=items), 200
    # section info not found (have to do something with this)
    return '', 404
