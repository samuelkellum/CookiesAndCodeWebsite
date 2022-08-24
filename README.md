This website was built to economize the acquisition of new members and increase member engagement for Cookies & Code, Tulane's premier Computer-Science club. The site is presently constructed with Django framework!

## Instructions for Getting Started Developing Locally: ##

### Setting up PostgreSQL and Project Local Database: ###

1) Open up your terminal and update brew with `brew update`
2) Install postgresql with `brew install postgresql`
3) Start postgres with `brew services start postgresql`
4) Open psql shell with `psql postgres`
  a) You may have to do `sudo -u postgres psql` (if you originally installed postgresql from the browser, you probably created 
  a root password, and you might need to enter that here)
5) In the shell, create a new user and password with `CREATE ROLE newUser WITH LOGIN PASSWORD ‘password’;`
6) Give [newUser] database creation capabilities with `ALTER ROLE newUser CREATEDB;`
7) Quit the shell with `\q`
8) Login as your new user with `psql postgres -U newuser` (this is how you should login in the future)
9) Create a main local database for the project with the following commands in the psql shell:
  a) `CREATE DATABASE databaseName;`
  b) `ALTER ROLE newuser SET client_encoding to ‘utf8’;`
  c) `ALTER ROLE newuser SET default_transaction_isolation TO ‘read committed’;`
  d) `ALTER ROLE newuser SET timezone to ‘[insert your timezone code]’;`
  e) `GRANT ALL PRIVILEGES ON DATABASE databasename TO newuser;`




