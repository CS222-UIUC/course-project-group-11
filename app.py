""" Modules required to handle the backend """
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classkonnect.ckulwu8pg879.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'takashi_yd'
app.config['MYSQL_PASSWORD'] = 'cU5SbJW6BCoLHmcyXe7n'
app.config['MYSQL_DB'] = 'classkonnect'
mysql = MySQL(app)

# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
@app.route('/')
def index():
    """Route for /"""
    return render_template("index.html"), 200

@app.route('/main', methods=["GET", "POST"])
def main():
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
            sub_subquery = ''
            for course in courses:
                query3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
                cursor.execute(query3)
                section = cursor.fetchall()
                enrollment_info.append(section)
                if course == courses[0]:
                    sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
                else:
                    sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
            required_info.append(enrollment_info)
            # fetch the top 5 most similar students to the logged in user
            subquery = f''' WHERE netId NOT LIKE '{items['netid']}' AND ({sub_subquery}) '''
            query4 = f''' SELECT netId, COUNT(*) as dupCount FROM classkonnect.enrollments {subquery} GROUP BY netId ORDER BY dupCount DESC LIMIT 5; '''
            cursor.execute(query4)
            # print(query4)
            other_users = cursor.fetchall()
            required_info.append(other_users)
            cursor.close()
            return render_template("main.html", items=required_info), 200
        # log-in failed
        return render_template("error.html", items=['Either your NetID or Password is wrong!']), 404
    if len(items) == 34: # registration
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
                        enrollment_info.append(section)
                        # populate enrollments table
                        query3 = f''' INSERT INTO classkonnect.enrollments (netId, CRN) VALUES ('{items['netid']}', {items[n_crn]}); '''
                        cursor.execute(query3)
                        mysql.connection.commit()
                    elif items[n_course] != '' and items[n_section] != '':
                        # need to adjust course name and section number the user put
                        adjusted_course = items[n_course].upper().replace(' ', '')
                        sub_id = adjusted_course[:-3] # e.g., CS
                        course_num = int(adjusted_course.replace(sub_id, '')) # e.g., 222
                        section_num = items[n_section].upper().replace(' ', '') # e.g., SL1
                        query2 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{sub_id}' AND CourseNumber = {course_num} AND SectionNumber = '{section_num}'; '''
                        cursor.execute(query2)
                        crn = cursor.fetchall()
                        if len(crn) == 0:
                            # course info not found (invalid entry)
                            error_message = f'You entered invalid course info for course{i}'
                        section = ((sub_id, course_num, section_num),)
                        enrollment_info.append(section)
                        # populate enrollments table
                        query3 = f''' INSERT INTO classkonnect.enrollments (netId, CRN) VALUES ('{items['netid']}', {crn[0][0]}); '''
                        cursor.execute(query3)
                        mysql.connection.commit()
                    else:
                        break
                required_info.append(enrollment_info)
                # populate users table on DB
                query = f''' INSERT INTO classkonnect.users (netId, password, discId) VALUES ('{items["netid"]}', '{items["pw"]}', '{items["discId"]}'); '''
                cursor.execute(query)
                mysql.connection.commit()
                que2 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{items["netid"]}'; '''
                cursor.execute(que2)
                courses = cursor.fetchall()
                sub_subquery = ''
                for course in courses:
                    que3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
                    cursor.execute(que3)
                    if course == courses[0]:
                        sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
                    else:
                        sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
                # fetch the top 5 most similar students to the logged in user
                subquery = f''' WHERE netId NOT LIKE '{items['netid']}' AND ({sub_subquery}) '''
                query4 = f''' SELECT netId, COUNT(*) as dupCount FROM classkonnect.enrollments {subquery} GROUP BY netId ORDER BY dupCount DESC LIMIT 5; '''
                cursor.execute(query4)
                other_users = cursor.fetchall()
                required_info.append(other_users)
                cursor.close()
                return render_template("main.html", items=required_info), 200
        # registration failed
        return render_template("error.html", items=[error_message]), 404
    error_message = 'No one should reach here!'
    return render_template("error.html", items=[error_message]), 404

@app.route('/main/<net_id>', methods=["GET", "POST"])
def main_user(net_id):
    """
        Route for the main page with the netid
    """
    required_info = []
    required_info.append(net_id)
    cursor = mysql.connection.cursor()
    query2 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
    cursor.execute(query2)
    courses = cursor.fetchall()
    enrollment_info = []
    sub_subquery = ''
    for course in courses:
        query3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
        cursor.execute(query3)
        section = cursor.fetchall()
        enrollment_info.append(section)
        if course == courses[0]:
            sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
        else:
            sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
    required_info.append(enrollment_info)
    # fetch the top 5 most similar students to the logged in user
    subquery = f''' WHERE netId NOT LIKE '{net_id}' AND ({sub_subquery}) '''
    query4 = f''' SELECT netId FROM classkonnect.users WHERE netID NOT LIKE '{net_id}'; '''
    query4 = f''' SELECT netId, COUNT(*) as dupCount FROM classkonnect.enrollments {subquery} GROUP BY netId ORDER BY dupCount DESC LIMIT 5; '''
    cursor.execute(query4)
    other_users = cursor.fetchall()
    required_info.append(other_users)
    cursor.close()
    return render_template("main.html", items=required_info), 200

@app.route('/register', methods=["POST"])
def register():
    """ Route for /register
        This will take you to the registration page.
    """
    return render_template("register.html"), 200

@app.route('/user_info/<net_id>', methods=["POST"])
def user_info(net_id):
    """ Route for /user_info
        This shows user information.
    """
    cursor = mysql.connection.cursor()
    query = f''' SELECT netId, discId FROM classkonnect.users WHERE netId = '{net_id}'; '''
    cursor.execute(query)
    userinfo = cursor.fetchall()
    required_info = []
    required_info.append(userinfo[0][0])
    if userinfo[0][1] == '':
        required_info.append('N/A')
    else:
        required_info.append(userinfo[0][1])
    query2 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
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

@app.route('/section/<net_id>/<subject>/<course>/<section>', methods=["GET", "POST"])
def section_info(net_id, subject, course, section):
    """Route for /section"""
    cursor = mysql.connection.cursor()
    query = f''' SELECT * FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {course} AND SectionNumber = '{section}'; '''
    cursor.execute(query)
    sectioninfo = cursor.fetchall()
    if len(sectioninfo) == 0: # To cope with a minor bug
        if len(section) == 1:
            section = section + '  '
        else:
            section = section + ' '
        query = f''' SELECT * FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {course} AND SectionNumber = '{section}'; '''
        cursor.execute(query)
        sectioninfo = cursor.fetchall()
    cursor.close()
    return render_template("section.html", items=[net_id, sectioninfo[0]]), 200

@app.route('/search/<net_id>', methods=["POST"])
def search(net_id):
    """Route for /search"""
    # look up enrollments
    cursor = mysql.connection.cursor()
    query = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
    cursor.execute(query)
    courses = cursor.fetchall()
    required_info = []
    for course in courses:
        query2 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = '{course[0]}'; '''
        cursor.execute(query2)
        section = cursor.fetchall()
        required_info.append(section)
    cursor.close()
    required_info.append(net_id)
    return render_template("search.html", items=required_info), 200

@app.route('/result/<net_id>', methods=["POST"])
def class_search(net_id):
    """ Route for /result
        This shows the results of the multi-class search.
    """
    # multi-class search functionality
    items = request.form
    if len(items) == 0:
        error_message = 'Please select at least one course!'
        return render_template("main_error.html", items=[error_message, net_id]), 404
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
                subject = subject + letter
            if phase == 1:
                if letter == ' ':
                    phase = 2
                    continue
                number = number + letter
            if phase == 2:
                section = section + letter
        selected_courses.append((subject, number, section))
    if len(selected_courses) == 1:
        cursor = mysql.connection.cursor()
        query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[0][0]}' AND CourseNumber = {selected_courses[0][1]} AND SectionNumber = '{selected_courses[0][2]}'; '''
        cursor.execute(query)
        crn = cursor.fetchall()
        query2 = f''' SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn[0][0]} AND netId NOT LIKE '{net_id}'; '''
        cursor.execute(query2)
        users = cursor.fetchall()
        cursor.close()
        required_info = [net_id]
        required_info.append(users)
        return render_template("result.html", items=required_info), 200
    if len(selected_courses) == 2:
        cursor = mysql.connection.cursor()
        query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[0][0]}' AND CourseNumber = {selected_courses[0][1]} AND SectionNumber = '{selected_courses[0][2]}'; '''
        cursor.execute(query)
        crn1 = cursor.fetchall()
        query1 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{selected_courses[1][0]}' AND CourseNumber = {selected_courses[1][1]} AND SectionNumber = '{selected_courses[1][2]}'; '''
        cursor.execute(query1)
        crn2 = cursor.fetchall()
        query2 = f''' SELECT DISTINCT a.netId FROM (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn1[0][0]}) AS a INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn2[0][0]} AND netId NOT LIKE '{net_id}') AS b ON a.netId = b.netId; '''
        cursor.execute(query2)
        users = cursor.fetchall()
        cursor.close()
        required_info = [net_id]
        required_info.append(users)
        return render_template("result.html", items=required_info), 200
    if len(selected_courses) == 3:
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
        query3 = f''' SELECT DISTINCT c.netId FROM (SELECT DISTINCT a.netId FROM (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn1[0][0]}) AS a INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn2[0][0]} AND netId NOT LIKE '{net_id}') AS b ON a.netId = b.netId) AS q INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn3[0][0]}) AS c ON q.netId = c.netId; '''
        cursor.execute(query3)
        users = cursor.fetchall()
        cursor.close()
        required_info = [net_id]
        required_info.append(users)
        return render_template("result.html", items=required_info), 200
    if len(selected_courses) == 4:
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
        query4 = f''' SELECT DISTINCT d.netId FROM (SELECT DISTINCT c.netId FROM (SELECT DISTINCT a.netId FROM (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn1[0][0]}) AS a INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn2[0][0]} AND netId NOT LIKE '{net_id}') AS b ON a.netId = b.netId) AS q INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn3[0][0]}) AS c ON q.netId = c.netId) AS w INNER JOIN (SELECT netId FROM classkonnect.enrollments WHERE CRN = {crn4[0][0]}) AS d ON w.netId = d.netId; '''
        cursor.execute(query4)
        users = cursor.fetchall()
        cursor.close()
        required_info = [net_id]
        required_info.append(users)
        return render_template("result.html", items=required_info), 200
    # more than 4 courses selected!
    error_message = 'Please select 4 courses at most!'
    return render_template("main_error.html", items=[error_message, net_id]), 404

@app.route('/confirm/<net_id>', methods=["POST"])
def confirm(net_id):
    """
        Route for the page to confirm that a user wants to delete his/her account
    """
    return render_template("confirm.html", items=[net_id]), 200

@app.route('/delete/<net_id>', methods=["POST"])
def delete_account(net_id):
    """
        Route for the index page while deleting a user's account
    """
    cursor = mysql.connection.cursor()
    query = f''' DELETE FROM classkonnect.users WHERE netId = '{net_id}'; '''
    cursor.execute(query)
    mysql.connection.commit()
    query2 = f''' DELETE FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
    cursor.execute(query2)
    mysql.connection.commit()
    cursor.close()
    return render_template("index.html"), 200

@app.route('/update/<net_id>', methods=["POST"])
def update_courses(net_id):
    """
        Route for the update page
    """
    required_info = [net_id]
    cursor = mysql.connection.cursor()
    query2 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
    cursor.execute(query2)
    courses = cursor.fetchall()
    enrollment_info = []
    sub_subquery = ''
    for course in courses:
        query3 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
        cursor.execute(query3)
        section = cursor.fetchall()
        enrollment_info.append(section)
        if course == courses[0]:
            sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
        else:
            sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
    required_info.append(enrollment_info)
    cursor.close()
    return render_template("update.html", items=required_info), 200

@app.route('/update/<net_id>/<subject>/<course>/<section>', methods=["POST"])
def update_course_info(net_id, subject, course, section):
    """
        Route for the page to update enrollment info
    """
    return render_template("update_info.html", items=[net_id, subject, course, section]), 200

@app.route('/delete_course/<net_id>/<subject>/<cours>/<section>', methods=["POST"])
def delete_course(net_id, subject, cours, section):
    """
        Route for the page to update enrollment info
    """
    cursor = mysql.connection.cursor()
    query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {cours} AND SectionNumber = '{section}'; '''
    cursor.execute(query)
    crn = cursor.fetchall()
    if len(crn) == 0: # To cope with a minor bug
        if len(section) == 1:
            section = section + '  '
        else:
            section = section + ' '
        query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {cours} AND SectionNumber = '{section}'; '''
        cursor.execute(query)
        crn = cursor.fetchall()
    query2 = f''' DELETE FROM classkonnect.enrollments WHERE netId = '{net_id}' AND CRN = '{crn[0][0]}'; '''
    cursor.execute(query2)
    mysql.connection.commit()
    required_info = [net_id]
    query3 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
    cursor.execute(query3)
    courses = cursor.fetchall()
    enrollment_info = []
    sub_subquery = ''
    for course in courses:
        query4 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
        cursor.execute(query4)
        section = cursor.fetchall()
        enrollment_info.append(section)
        if course == courses[0]:
            sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
        else:
            sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
    required_info.append(enrollment_info)
    cursor.close()
    return render_template("update.html", items=required_info), 200

@app.route('/update_course/<net_id>/<subject>/<cours>/<section>', methods=["POST"])
def update_course(net_id, subject, cours, section):
    """
        Route for updatinng the course and showing the update page
    """
    items = request.form
    error_message = 'Something is wrong with the course info you entered!'
    if (items['crn1'] != '') or (items['course1'] != '' and items['sn1'] != ''):
        cursor = mysql.connection.cursor()
        n_crn = 'crn1'
        n_course = 'course1'
        n_section = 'sn1'
        if items[n_crn] != '': # from crn
            query2 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {items[n_crn]}; '''
            cursor.execute(query2)
            section = cursor.fetchall()
            if len(section) == 0:
                # course info not found (invalid entry)
                error_message = 'You entered invalid CRN for the new course!'
                return render_template("main_error.html", items=[error_message, net_id]), 404
            # update enrollments table when crn is valid
            obtain_crn_query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {cours} AND SectionNumber = '{section}'; '''
            cursor.execute(obtain_crn_query)
            original_crn = cursor.fetchall()
            query3 = f''' UPDATE classkonnect.enrollments SET CRN = {items[n_crn]} WHERE netId = '{net_id}' AND CRN = {original_crn[0][0]}; '''
            cursor.execute(query3)
            mysql.connection.commit()
        elif items[n_course] != '' and items[n_section] != '':
            # need to adjust course name and section number the user put
            adjusted_course = items[n_course].upper().replace(' ', '')
            sub_id = adjusted_course[:-3] # e.g., CS
            course_num = int(adjusted_course.replace(sub_id, '')) # e.g., 222
            section_num = items[n_section].upper().replace(' ', '') # e.g., SL1
            query2 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{sub_id}' AND CourseNumber = {course_num} AND SectionNumber = '{section_num}'; '''
            cursor.execute(query2)
            crn = cursor.fetchall()
            if len(crn) == 0:
                # course info not found (invalid entry)
                error_message = 'You entered invalid course info for the new course!'
                return render_template("main_error.html", items=[error_message, net_id]), 404
            # update enrollments table
            obtain_crn_query = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{subject}' AND CourseNumber = {cours} AND SectionNumber = '{section}'; '''
            cursor.execute(obtain_crn_query)
            original_crn = cursor.fetchall()
            query3 = f''' UPDATE classkonnect.enrollments SET CRN = {crn[0][0]} WHERE netId = '{net_id}' AND CRN = {original_crn[0][0]}; '''
            cursor.execute(query3)
            mysql.connection.commit()
        else:
            return render_template("main_error.html", items=[error_message, net_id]), 404
        required_info = [net_id]
        query3 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
        cursor.execute(query3)
        courses = cursor.fetchall()
        enrollment_info = []
        sub_subquery = ''
        for course in courses:
            query4 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
            cursor.execute(query4)
            section = cursor.fetchall()
            enrollment_info.append(section)
            if course == courses[0]:
                sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
            else:
                sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
        required_info.append(enrollment_info)
        cursor.close()
        return render_template("update.html", items=required_info), 200
    return render_template("main_error.html", items=[error_message, net_id]), 404

@app.route('/add_course/<net_id>', methods=["POST"])
def add_course(net_id):
    """
        Route for adding the course and showing the update page
    """
    items = request.form
    error_message = 'Something is wrong with the course info you entered!'
    if (items['crn2'] != '') or (items['course2'] != '' and items['sn2'] != ''):
        cursor = mysql.connection.cursor()
        n_crn = 'crn2'
        n_course = 'course2'
        n_section = 'sn2'
        if items[n_crn] != '': # from crn
            query2 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {items[n_crn]}; '''
            cursor.execute(query2)
            section = cursor.fetchall()
            if len(section) == 0:
                # course info not found (invalid entry)
                error_message = 'You entered invalid CRN for the new course!'
                return render_template("main_error.html", items=[error_message, net_id]), 404
            # insert enrollments table when crn is valid
            query3 = f''' INSERT INTO classkonnect.enrollments (netId, CRN) VALUES ('{net_id}', {items[n_crn]}); '''
            cursor.execute(query3)
            mysql.connection.commit()
        elif items[n_course] != '' and items[n_section] != '':
            # need to adjust course name and section number the user put
            adjusted_course = items[n_course].upper().replace(' ', '')
            sub_id = adjusted_course[:-3] # e.g., CS
            course_num = int(adjusted_course.replace(sub_id, '')) # e.g., 222
            section_num = items[n_section].upper().replace(' ', '') # e.g., SL1
            query2 = f''' SELECT CRN FROM classkonnect.courses WHERE SubjectId = '{sub_id}' AND CourseNumber = {course_num} AND SectionNumber = '{section_num}'; '''
            cursor.execute(query2)
            crn = cursor.fetchall()
            if len(crn) == 0:
                # course info not found (invalid entry)
                error_message = 'You entered invalid course info for the new course!'
                return render_template("main_error.html", items=[error_message, net_id]), 404
            # insert enrollments table
            query3 = f''' INSERT INTO classkonnect.enrollments (netId, CRN) VALUES ('{net_id}', {crn[0][0]}); '''
            cursor.execute(query3)
            mysql.connection.commit()
        else:
            return render_template("main_error.html", items=[error_message, net_id]), 404
        required_info = [net_id]
        query3 = f''' SELECT CRN FROM classkonnect.enrollments WHERE netId = '{net_id}'; '''
        cursor.execute(query3)
        courses = cursor.fetchall()
        enrollment_info = []
        sub_subquery = ''
        for course in courses:
            query4 = f''' SELECT SubjectId, CourseNumber, SectionNumber FROM classkonnect.courses WHERE CRN = {course[0]}; '''
            cursor.execute(query4)
            section = cursor.fetchall()
            enrollment_info.append(section)
            if course == courses[0]:
                sub_subquery = sub_subquery + 'CRN = ' + str(course[0])
            else:
                sub_subquery = sub_subquery + ' OR CRN = ' + str(course[0])
        required_info.append(enrollment_info)
        cursor.close()
        return render_template("update.html", items=required_info), 200
    return render_template("main_error.html", items=[error_message, net_id]), 404
