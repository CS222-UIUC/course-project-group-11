""" Modules required to handle the backend """
from distutils.log import error
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classkonnect.ckulwu8pg879.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'takashi_yd'
app.config['MYSQL_PASSWORD'] = 'cU5SbJW6BCoLHmcyXe7n'
app.config['MYSQL_DB'] = 'classkonnect'
mysql = MySQL(app)

# pylint: disable=line-too-long
@app.route('/')
def index():
    """Route for /"""
    return render_template("index.html"), 200

@app.route('/main', methods=["POST"])
def user():
    """Route for /main"""
    items = request.form
    if len(items) == 2: # log_in
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
                query3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
                cursor.execute(query3)
                section = cursor.fetchall()
                enrollment_info.append(section)
            required_info.append(enrollment_info)
            # we're supposed to run a complex query here to obtain a list of similar students
            # for now, I will just list up some users to display user info
            query4 = f''' SELECT netId FROM classkonnect.users WHERE netID NOT LIKE '{items['netid']}' LIMIT 2; '''
            cursor.execute(query4)
            other_users = cursor.fetchall()
            required_info.append(other_users)
            cursor.close()
            return render_template("main.html", items=required_info), 200
        # log-in failed
        return render_template("error.html", items=['Either your NetID or Password is wrong!']), 404
    elif len(items) == 34: # registration
        items = request.form
        error_message = 'Passwords do not match!'
        # see if the user provided the same password twice
        if items['pw'] == items['pwa']:
            error_message = 'You must register at least one course you are enrolled in!'
            # see if at least one course info was provided by the user
            if (items['crn1'] != '') or (items['course1'] != '' and items['sn1'] != ''):
                required_info = []
                required_info.append(items["netid"])
                cursor = mysql.connection.cursor()
                enrollment_info = []
                for i in range(1, 11):
                    n_crn = f'crn{i}'
                    n_course = f'course{i}'
                    n_section = f'sn{i}'
                    if items[n_crn] != '':
                        query2 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = '{items[n_crn]}'; '''
                        cursor.execute(query2)
                        section = cursor.fetchall()
                        if len(section) == 0:
                            # course info not found (invalid entry)
                            error_message = f'You entered invalid CRN for course{i}'
                            return render_template("error.html", items=[error_message]), 404
                        enrollment_info.append(section)
                        # populate enrollments table
                        query3 = f''' INSERT INTO classkonnect.enrollments (netId, CRN) VALUES ('{items['netid']}', {items[n_crn]}); '''
                        cursor.execute(query3)
                        mysql.connection.commit()
                    elif items[n_course] != '' and items[n_section] != '':
                        # need to adjust course name and section number the user put
                        adjusted_course = items[n_course].upper().replace(' ', '')
                        subId = adjusted_course[:-3] # e.g., CS
                        course_num = int(adjusted_course.replace(subId, '')) # e.g., 222
                        section_num = items[n_section].upper().replace(' ', '') # e.g., SL1
                        query2 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{subId}' AND CourseNumber = {course_num} AND SectionNumber = '{section_num}'; '''
                        cursor.execute(query2)
                        crn = cursor.fetchall()
                        if len(crn) == 0:
                            # course info not found (invalid entry)
                            error_message = f'You entered invalid course info for course{i}'
                            return render_template("error.html", items=[error_message]), 404
                        section = ((subId, course_num, section_num),)
                        enrollment_info.append(section)
                        # populate enrollments table
                        query3 = f''' INSERT INTO classkonnect.enrollments (netId, CRN) VALUES ('{items['netid']}', {crn[0]}); '''
                        cursor.execute(query3)
                        mysql.connection.commit()
                    else:
                        break
                required_info.append(enrollment_info)
                # populate users table on DB
                query = f''' INSERT INTO classkonnect.users (netId, password, discId) VALUES ('{items["netid"]}', '{items["pw"]}', '{items["discId"]}'); '''
                cursor.execute(query)
                mysql.connection.commit()
                cursor.close()
                # we're supposed to run a complex query here to obtain a list of similar students
                return render_template("main.html", items=required_info), 200
        # registration failed
        return render_template("error.html", items=[error_message]), 404

@app.route('/register', methods=["POST"])
def register():
    """ Route for /register
        This will take you to the registration page.
    """
    return render_template("register.html"), 200

@app.route('/user_info/<netID>', methods=["POST"])
def user_info(netID):
    """ Route for /user_info
        This shows user information.
    """
    cursor = mysql.connection.cursor()
    query = f''' SELECT netId, discId FROM classkonnect.users WHERE netId = '{netID}'; '''
    cursor.execute(query)
    userinfo = cursor.fetchall()
    required_info = []
    required_info.append(userinfo[0][0])
    if userinfo[0][1] == '':
        required_info.append('N/A')
    else:
        required_info.append(userinfo[0][1])
    query2 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{netID}'; '''
    cursor.execute(query2)
    courses = cursor.fetchall()
    enrollment_info = []
    for course in courses:
        query3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = '{course[0]}'; '''
        cursor.execute(query3)
        section = cursor.fetchall()
        enrollment_info.append(section)
    required_info.append(enrollment_info)
    cursor.close()
    return render_template("user_info.html", items=required_info), 200

@app.route('/section/<subject>/<course>/<section>', methods=["GET", "POST"])
def section_info(subject, course, section):
    """Route for /section"""
    cursor = mysql.connection.cursor()
    query = f''' SELECT * FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {course} AND SectionNumber = '{section}'; '''
    cursor.execute(query)
    sectioninfo = cursor.fetchall()
    if len(sectioninfo) == 0: # To cope with a minor bug
        section = section + ' '
        query = f''' SELECT * FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {course} AND SectionNumber = '{section}'; '''
        cursor.execute(query)
        sectioninfo = cursor.fetchall()
    cursor.close()
    return render_template("section.html", items=sectioninfo[0]), 200

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
    required_info.append(user)
    return render_template("search.html", items=required_info), 200

@app.route('/result/<user>', methods=["POST"])
def class_search(user):
    # multi-class search functionality
    items = request.form
    if len(items) == 0:
        error_message = 'Please select at least one course!'
        return render_template("search_error.html", items=[error_message, user]), 404
    else:
        selected_courses = []
        for item in items:
            subject = ''
            number = ''
            section = ''
            phase = 0
            for letter in item:
                if phase == 0:
                    if letter == ' ':
                        phase = 1
                        continue
                    else:
                        subject = subject + letter
                if phase == 1:
                    if letter == ' ':
                        phase = 2
                        continue
                    else:
                        number = number + letter
                if phase == 2:
                    section = section + letter
            selected_courses.append((subject, number, section))
        if len(selected_courses) == 1:
            cursor = mysql.connection.cursor()
            query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[0][0]}' AND CourseNumber = {selected_courses[0][1]} AND SectionNumber = '{selected_courses[0][2]}'; '''
            cursor.execute(query)
            crn = cursor.fetchall()
            query2 = f''' SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn[0][0]} AND netId NOT LIKE '{user}'; '''
            cursor.execute(query2)
            users = cursor.fetchall()
            cursor.close()
            required_info = []
            required_info.append(users)
            return render_template("result.html", items=required_info), 200
        elif len(selected_courses) == 2:
            cursor = mysql.connection.cursor()
            query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[0][0]}' AND CourseNumber = {selected_courses[0][1]} AND SectionNumber = '{selected_courses[0][2]}'; '''
            cursor.execute(query)
            crn1 = cursor.fetchall()
            query1 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[1][0]}' AND CourseNumber = {selected_courses[1][1]} AND SectionNumber = '{selected_courses[1][2]}'; '''
            cursor.execute(query1)
            crn2 = cursor.fetchall()
            query2 = f''' SELECT DISTINCT a.netId FROM (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn1[0][0]}) AS a INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn2[0][0]} AND netId NOT LIKE '{user}') AS b ON a.netId = b.netId; '''
            cursor.execute(query2)
            users = cursor.fetchall()
            cursor.close()
            required_info = []
            required_info.append(users)
            return render_template("result.html", items=required_info), 200
        elif len(selected_courses) == 3:
            cursor = mysql.connection.cursor()
            query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[0][0]}' AND CourseNumber = {selected_courses[0][1]} AND SectionNumber = '{selected_courses[0][2]}'; '''
            cursor.execute(query)
            crn1 = cursor.fetchall()
            query1 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[1][0]}' AND CourseNumber = {selected_courses[1][1]} AND SectionNumber = '{selected_courses[1][2]}'; '''
            cursor.execute(query1)
            crn2 = cursor.fetchall()
            query2 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[2][0]}' AND CourseNumber = {selected_courses[2][1]} AND SectionNumber = '{selected_courses[2][2]}'; '''
            cursor.execute(query2)
            crn3 = cursor.fetchall()
            query3 = f''' SELECT DISTINCT c.netId FROM (SELECT DISTINCT a.netId FROM (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn1[0][0]}) AS a INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn2[0][0]} AND netId NOT LIKE '{user}') AS b ON a.netId = b.netId) AS q INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn3[0][0]}) AS c ON q.netId = c.netId; '''
            cursor.execute(query3)
            users = cursor.fetchall()
            cursor.close()
            required_info = []
            required_info.append(users)
            return render_template("result.html", items=required_info), 200
        elif len(selected_courses) == 4:
            cursor = mysql.connection.cursor()
            query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[0][0]}' AND CourseNumber = {selected_courses[0][1]} AND SectionNumber = '{selected_courses[0][2]}'; '''
            cursor.execute(query)
            crn1 = cursor.fetchall()
            query1 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[1][0]}' AND CourseNumber = {selected_courses[1][1]} AND SectionNumber = '{selected_courses[1][2]}'; '''
            cursor.execute(query1)
            crn2 = cursor.fetchall()
            query2 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[2][0]}' AND CourseNumber = {selected_courses[2][1]} AND SectionNumber = '{selected_courses[2][2]}'; '''
            cursor.execute(query2)
            crn3 = cursor.fetchall()
            query3 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[3][0]}' AND CourseNumber = {selected_courses[3][1]} AND SectionNumber = '{selected_courses[3][2]}'; '''
            cursor.execute(query3)
            crn4 = cursor.fetchall()
            query4 = f''' SELECT DISTINCT d.netId FROM (SELECT DISTINCT c.netId FROM (SELECT DISTINCT a.netId FROM (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn1[0][0]}) AS a INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn2[0][0]} AND netId NOT LIKE '{user}') AS b ON a.netId = b.netId) AS q INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn3[0][0]}) AS c ON q.netId = c.netId) AS w INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn4[0][0]}) AS d ON w.netId = d.netId; '''
            cursor.execute(query4)
            users = cursor.fetchall()
            cursor.close()
            required_info = []
            required_info.append(users)
            return render_template("result.html", items=required_info), 200
        else: # more than 4 courses selected!
            error_message = 'Please select 5 courses at most!'
            return render_template("search_error.html", items=error_message), 404
