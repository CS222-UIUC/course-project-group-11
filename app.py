""" Modules required to handle the backend """
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classkonnect.ckulwu8pg879.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'takashi_yd'
app.config['MYSQL_PASSWORD'] = 'cU5SbJW6BCoLHmcyXe7n'
app.config['MYSQL_DB'] = 'classkonnect'
mysql = MySQL(app)

# this lcoal database contains three tables with the following pieces of data:
# users (netID, pw, discID)
#       ('yoda2', '1234', 'Yoda#1234')
#       ('guest', '1234', '')
#       ('inst', '1234', '')
# enrollments (netID, CRN)
#             ('yoda2', 74484), ('yoda2', 35917), ('yoda2', 63733), ('yoda2', 35030)
#             ('guest', 74484), ('guest', 35917), ('guest', 59328), ('guest', 63037)
#             ('inst', 74484), ('inst', 77096), ('inst', 66445), ('inst', 35030)
# courses: now this table contains the exact same elements as the csv file

# pylint: disable=line-too-long
@app.route('/')
def index():
    """Route for /"""
    return render_template("index.html"), 200

@app.route('/main', methods=["POST"])
def user_login():
    """Route for /main"""
    items = request.form
    cursor = mysql.connection.cursor()
    query = f''' SELECT netId, password FROM classkonnect.users WHERE netId = '{items['netid']}' AND password = '{items['pw']}'; '''
    cursor.execute(query)
    user = cursor.fetchall()
    if len(user) == 1:
        required_info = []
        required_info.append(items["netid"])
        query2 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{items["netid"]}'; '''
        cursor.execute(query2)
        courses = cursor.fetchall()
        enrollment_info = []
        for course in courses:
            query3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = '{course[0]}'; '''
            cursor.execute(query3)
            section = cursor.fetchall()
            enrollment_info.append(section)
        required_info.append(enrollment_info)
        # we're supposed to run a complex query here to obtain a list of similar students
        #
        #
        cursor.close()
        return render_template("main.html", items=required_info), 200
    # log-in failed
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

# @app.route('/section/<course>/<section>', methods=["POST"])
# def section_info(course, section):
#     """Route for /section"""
#     # look up a section info
#     # for sec in sections:
#     #     course_num = sec['subjectId'] + sec['courseNum']
#     #     if course_num == course and sec['sectionNum'] == section:
#     #         items = sec
#     #         return render_template("section.html", items=items), 200
#     # section info not found (have to do something with this)
#     return '', 404

@app.route('/search/<user>', methods=["POST"])
def search(user):
    """Route for /search"""
    # look up enrollments
    cursor = mysql.connection.cursor()
    query = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{user}'; '''
    cursor.execute(query)
    courses = cursor.fetchall()
    required_info = []
    for course in courses:
        query2 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = '{course[0]}'; '''
        cursor.execute(query2)
        section = cursor.fetchall()
        required_info.append(section)
    cursor.close()
    return render_template("search.html", items=required_info), 200

@app.route('/search/<user>', methods=["POST"])
def section_info(user):
    """Route for /search"""