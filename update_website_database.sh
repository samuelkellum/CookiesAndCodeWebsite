#!/bin/zsh

# Set all local environment variables located in .env file
# ---------------------------------------------------------
python -c 'from dotenv import load_dotenv; load_dotenv()' # for Python

set -a # automatically export all variables
source .env
set +a

# Overwrite local database with contents of remote heroku one
# ------------------------------------------------------------
rm *.dump *.dump.* # delete all previous dump files
heroku pg:backups:capture -a cookies-and-code-site # create a backup of the Heroku remote database
heroku pg:backups:download -a cookies-and-code-site # download the backup
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U bennett -d candctu latest.dump	


# Run scripts to add new users and update events
# ----------------------------------------------
python manage.py runscript add_wavesync_members --script-args $1 # add new users
python manage.py runscript google_test # update events

# Overwrite remote heroku database with contents of local one
# -----------------------------------------------------------
pg_dump -Fc --no-acl --no-owner -h localhost -U bennett candctu > mydb1.dump # dump local database to compressed .dump file
aws s3api put-object --bucket cookies-and-code-s3-bucket --key mydb1.dump --body mydb1.dump # hard-coded bucket name is okay as stated here: https://security.stackexchange.com/questions/214499/s3-bucket-name-obscurity-as-security
SIGNED_URL=$(aws s3 presign s3://cookies-and-code-s3-bucket/mydb1.dump)
heroku pg:backups:restore $SIGNED_URL DATABASE_URL --app cookies-and-code-site --confirm cookies-and-code-site