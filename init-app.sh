#! /bin/sh

set -o errexit
set -o nounset 

echo "Checking dependencies..."

cd db
sh ./init-db.sh
cd ..

echo "Starting app in dir ${PWD}"
FLASK_ENV=development FLASK_APP=lapso/app.py flask run --host="0.0.0.0"
