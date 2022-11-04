# ClassKonnect (Group 11 project in CS 222)

### [our proposal](https://docs.google.com/document/d/1UTmIv_weaekLc5lBQdIZ6UTJ0D-l6-Cf1y4TpaT1hT0/edit)

# Update on Nov 4
I populated 10 additional users with valid enrollments to the database so that we have more understanding on how this web app works. Also, I have implemented the multi-class search functionality although this is not still perfect in that the program cannot handle more than 3 multiple class seraches. Next week, I will focus on finalizing this functionality.

### Legacy statements

# Update on Oct 28
I implemented the functionality to display courses and users info when you click on a button associated with either of them, fetching data from the SQL database (see screenshots below)

When you click on a course button [ CS 222 SL1 ]
<img src="/static/img/course1.png" alt="users" style="height: 250px; width:2276px;"/>

When you click on a course button [ STAT 400 YL1 ]
<img src="/static/img/course2.png" alt="users" style="height: 250px; width:2276px;"/>

When you click on a user button [ guest ]
<img src="/static/img/user1.png" alt="users" style="height: 250px; width:2276px;"/>

When you click on a user button [ inst ]
<img src="/static/img/user2.png" alt="users" style="height: 250px; width:2276px;"/>

Also, I successfully implemented the user registration system although it was not assigned to me because this task, I am sure, is tough. Screenshots below are the registration pages (what users should put in the webpage to populate our DB with the user input). Basically, users should provide either (1) CRN or (2) a combination of a course name and a section name.

To register info on 'guest2'
<img src="/static/img/guest2.png" alt="users" style="height: 250px; width:2276px;"/>

To register info on 'guest3'
<img src="/static/img/guest3.png" alt="users" style="height: 250px; width:2276px;"/>

After populating the users and enrollments tables by registering users, now those tables look like the following:

Users
<img src="/static/img/users.png" alt="users" style="height: 250px; width:1276px;"/>

Enrollments

<img src="/static/img/enrollments.png" alt="test_coverage" style="height: 480px; width:176px;"/>

# Update on Oct 21
I decided to make my SQL server on AWS available to anyone who has access to this PR/repo so serious security concerns aside, we can all access the same DB on AWS at least in `app.py`.

# You can explore SQL queries to interact with the server but NEVER RUN A QUERY WHICH CONTAINS THE WORD 'DELETE' OR 'UPDATE'

I also implemented a UI for class search feature from which you can look up users who are taking a course or a combination of courses from the courses you are taking. To do so, once you log in (refer to the users table shown below), you will see a button 'Class Search' so you cannot miss it.

Class Search
<img src="/static/img/search.png" alt="users" style="height: 250px; width:2276px;"/>

## Oct 7 or 14
I managed to extract info on every section of every course offered at UIUC in Fall 2022 from Course Explorer API. Refer to `course_extractor.ipynb`. If you run each cell in the jupyter notebook, you will obtain `fall2022_courses.csv` which is exactly what we need. Now that it is just a few steps away from setting up a database, I guess each of us can set it up locally. I consider setting it up on AWS so that we all can interact with the DB.

## Requirements
Refer to the `requirements.txt` file.

## How to get started
```bash
cd course-project-group11
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask run
```

## For the frontend developers
Feel free to edit the HTML/CSS files in the `static` and `templates` folders.
`base.html` serves as a template for the `main.html` and other html files created in the future.
`index.html` is solely for users to log in or sign up. Since there should not be the "Your Friends" banner on that page, the html file does not use the aforementioned template file.
`main.html` will be the very first screen users will see once logged in or signed up.

## Test Coverage
We are still having difficulty in using pytest for testing a flask web app, but here's the result of running the following command: `pytest --cov --cov-branch -v test.py`

<img src="/static/img/test_cov_week1.png" alt="test_coverage" style="height: 250px; width:2276px;"/>
