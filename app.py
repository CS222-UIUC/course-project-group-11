""" Modules required to handle the backend """
from flask import Flask, render_template, request

app = Flask(__name__)

# for the time being, we will hold a piece of data for development here and later delete
# and replace it with actual data from our database

# netid and pw
login_info = {"guest": "1234",
              "XXX": "0000",
              "YYY": "0000",
              "ZZZ": "0000"}
# user_name -> list of courses he or she is taking
user_info = {"guest": {"courses": ["CS225", "CS222", "CS233", "MATH415", "STAT400"]},
             "XXX": {"courses": ["CS374", "CS440", "CS341", "CS498"]},
             "YYY": {"courses": ["CS128", "MATH231", "CS173"]},
             "ZZZ": {"courses": ["CS225", "CS222", "CS233", "STAT410"]}}



@app.route('/')
def index():
    """Route for /"""
    return render_template("index.html"), 200

@app.route('/main', methods=["POST"])
def user_login():
    """Route for /main"""
    items = request.form
    if items["netid"] in login_info:
        if items["pw"] == login_info[items["netid"]]:
            # successfully logged in
            required_info = []
            # here, we're supposed to manipulate data, writing queries and so on
            # but due to the issue where we don't have any solid idea as to
            # how to host a web/SQL server
            required_info.append(items["netid"])
            required_info.append(user_info[items["netid"]])
            required_info.append(list(login_info.keys())[1:])
            return render_template("main.html", items=required_info), 200
    # did not successfully logged in (have to do something with this)
    return "", 404

@app.route('/temp', methods=["GET"])
def temp():
    """This route is still under construction and
    shows almost nothing but later will be developed"""
    return render_template("base.html"), 200

@app.route('/register', methods=["POST"])
def register():
    """This route is still under construction and
    shows almost nothing but later will be dev"""
    # return "reached", 200
    return render_template("register.html"), 200

# @app.route('/lookup/<course>', methods=["GET"])
# def courses(course):
#     """Route for /lookup"""
#     fake_enrollments = ["CS225", "CS222", "MATH415", "CS233", "STAT400"]
#     if course in fake_enrollments:
#         return '', 200
#     return '', 404

# @app.route('/enrollment', methods=["POST"])
# def enrollment():
#     """Route for /enrollment"""
#     requested_course = request.form['subject'] + request.form['number']
#     server_url = os.getenv('BASE_URL')
#     req = requests.get(f'{server_url}/lookup/{requested_course}')
#     if req.status_code == 200:
#         found = "We confirmed that you're enrolled in " + requested_course + "!"
#         return found, 200
#     return '', 404
