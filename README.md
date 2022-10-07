# ClassKonnect (Group 11 project in CS 222)

### [our proposal](https://docs.google.com/document/d/1UTmIv_weaekLc5lBQdIZ6UTJ0D-l6-Cf1y4TpaT1hT0/edit)

# Update on Oct 7
For now, we do not use SQL databases because we have not agreed on how to host the databases (if we are allowed to set up and interact with databases locally, never in a production environment, we will take that route). Thus, as global variables, we put some random user information and course information. In the log-in page, hence, put 'guest' as our NetID and '1234' as our password.

Update:
I managed to extract info on every section of every course offered at UIUC in Fall 2022 from Course Explorer API. Refer to `course_extractor.ipynb`. If you run each cell in the jupyter notebook, you will obtain `fall2022_courses.csv` which is exactly what we need. Now that it is just a few steps away from setting up a database, I guess each of us can set it up locally. I consider setting it up on AWS so that we all can interact with the DB.

Also, when you click on the course button (CS222 SL1 specifically), sample course/section information on CS222 SL1 will show up. For other courses, it won't work at this time.

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
