## Journal App

A simple journal application where you can create an account, create and edit journal posts, and then publish them for all to see.
You can also unpublish and delete posts altogether.

Hosted for free on Render, so it's a little on the slow side. <br>
Live link: https://journal-app-0nnw.onrender.com/

### Features
- Account creating and deleting
- Post creating, editing, publishing, unpublishing, and deleting

### Planned Features
- Likes
- Comments

### Current tasks
- Reimplement testing, especially using Github Actions for CI
- Add more testing, such as integration tests


### Technologies
- Flask for application backend and routing
- Postgresql for database management
- Flask sessions for user authentication
- bcrypt for password encryption
- Regex for username and password limitations and restrictions

  

#### Instructions for running locally

clone project using git <br>
`git clone https://github.com/benhurst1/journal_app.git journal_app`

create a virtual environment using venv <br>
`python3 -m venv venv`

activate the virtual environment <br>
`source venv/bin/activate`

install the requirements <br>
`pip install -r requirements.txt`

create database <br>
`createdb journal_app`

seed the tables into the database <br>
`psql journal_app < seeds/setup.sql`

Run the development server <br>
`flask run`
