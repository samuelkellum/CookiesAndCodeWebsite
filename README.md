This website was built to economize the acquisition of new members and increase member engagement for Cookies & Code, Tulane's premier Computer-Science club. The site is presently constructed with Django framework!

## Instructions for Getting Started Developing Locally: ##

### Setting up PostgreSQL and Project Local Database: ###

1. Open up your terminal and update brew with `brew update`
2. Install postgresql with `brew install postgresql`
3. Start postgres with `brew services start postgresql`
4. Open psql shell with `psql postgres`
    1. You may have to do `sudo -u postgres psql` (if you originally installed postgresql from the browser, you probably created a root password, and you might need to enter that here)
5. In the shell, create a new user and password with `CREATE ROLE newUser WITH LOGIN PASSWORD ‘password’;`
6. Give [newUser] database creation capabilities with `ALTER ROLE newUser CREATEDB;`
7. Quit the shell with `\q`
8. Login as your new user with `psql postgres -U newuser` (this is how you should login in the future)
9. Create a main local database for the project with the following commands in the psql shell:
    1. `CREATE DATABASE databaseName;`
    2. `ALTER ROLE newuser SET client_encoding to ‘utf8’;`
    3. `ALTER ROLE newuser SET default_transaction_isolation TO ‘read committed’;`
    4. `ALTER ROLE newuser SET timezone to ‘[insert your timezone code]’;`
    5. `GRANT ALL PRIVILEGES ON DATABASE databasename TO newuser;`


### Setting up Project: ###

1. Open up your terminal and navigate to the directory in which you want to store the project (we recommend the home (~) directory) with `cd [desired directory]`
2. Clone the project from our Github repository with  `git clone https://github.com/samuelkellum/CookiesAndCodeWebsite.git`
3. Navigate to the project directory with `cd CookiesAndCodeWebsite`
4. Create a virtual environment with `python3 -m venv env`
5. Start environment with `source env/bin/activate`
6. Install all required packages for the project with `pip install -r requirements.txt`
7. In `CookiesAndCodeWebsite/settings.py` add your local database to the DATABASES dictionary following the following same pattern as the ones in there. Give the new entry a key (databaseKEY) and be sure to replace ‘NAME,’ ‘USER,’ and ‘PASSWORD’ with whatever you set your databaseName, newUser, and password as in “Setting up PostgresSQL”
9. In the terminal, set the environment variable for the database with `export DJANGO_DATABASE=’databaseKEY’`
10. Populate your local database. 
    1. In the terminal, make and apply the migrations in main/models.py with `python3 manage.py makemigrations` then `python3 manage.py migrate`
    2. Create a data directory in your project root directory with `mkdir data`
    3. Move the club's roster CSV file into the data directory
    4. Run the script for creating all user profiles with `python3 manage.py runscript add_wavesync_members`
11. Create a superuser with `python3 manage.py createsuperuser`
    1. Enter an email and password. (Make sure to remember your password! You will need this to access the ever-so important admin page!)
12. With a database populated and superuser created, the website is ready to view. For local server purposes, we will use Heroku's `heroku local` command (the website is hosted on Heroku, so it makes sense to use Heroku here). [Install the Heroku Command Line Interface](https://devcenter.heroku.com/articles/heroku-cli)--for a Mac, `brew tap heroku/brew && brew install heroku` should work. 
13. Heroku requires a .env file from which it reads environment variables. Create a .env file in the project root directory with `touch .env`. Add the below lines to .env:
    1. DEBUG_VALUE="True"
    2. PORT=8000
    3. DJANGO_DATABASE='[databaseKEY]'
14. Django projects require a secrete key. Create and append a randomly-generated secret key to .env with `echo “SECRET_KEY=$(openssl rand -base64 32)” >> .env`
15. Run `heroku local` to start the server
16. In your browser of choice, navigate to http://127.0.0.1:8000/admin/ and login with the superuser credentials you created.
17. Click “View Site” in the top right of the webpage. You should now have access to a working website!






