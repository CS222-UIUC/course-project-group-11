""" Modules required to handle the backend """
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password' # password should be the pw for your local SQL server
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
# courses (subjectID, courseID, courseName, CRN)
#         ('STAT', 400, 'Statistics and Probability I', 35030)
#         ('CS', 225, 'Data Structures', 35917)
#         ('MATH', 241, 'Calculus III', 59328)
#         ('MATH', 415, 'Applied Linear Algebra', 63037)
#         ('CS', 233, 'Computer Architecture', 63733)
#         ('CS', 361, 'Probability & Statistics for Computer Science', 66298)
#         ('CS', 374, 'Introduction to Algorithms & Models of Computation', 66445)
#         ('CS', 222, 'Software Design Lab', 74484)
#         ('CS', 340, 'Introduction to Computer Systems', 77096)

# pylint: disable=line-too-long
@app.route('/')
def index():
    """Route for /"""
    return render_template("index.html"), 200

@app.route('/main', methods=["POST"])
def user_login():
    """Route for /main"""
    items = request.form
    # if items["netid"] in users:
    #     if items["pw"] == users[items["netid"]]['pw']:
    #         # successfully logged in
    #         required_info = []
    #         # here, we're supposed to manipulate data, writing queries and so on
    #         # but due to the issue where we don't have any solid idea as to
    #         # how to host a web/SQL server
    #         required_info.append(items["netid"])
    #         required_info.append(users[items["netid"]]['courses'])
    #         required_info.append(list(users.keys())[1:])
    #         return render_template("main.html", items=required_info), 200
    # # did not successfully logged in (have to do something with this)
    # return render_template("error.html"), 404
    cursor = mysql.connection.cursor()
    query = ''' SELECT netID, pw FROM classkonnect.users; '''
    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        if user[0] == items['netid'] and user[1] == items['pw']:
            # successfully logged in
            required_info = []
            required_info.append(items["netid"])
            # query2 = '''  '''
            # cursor.execute()
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
