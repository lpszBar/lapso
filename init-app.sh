#! /bin/sh

set -o errexit
set -o nounset 

echo "Checking dependencies..."

cd db
sh ./init-db.sh
cd ..

#cd static && (npm start &) && cd ..

cd lapso
echo "Starting app in dir ${PWD}"
FLASK_ENV=development FLASK_APP=app.py flask run --host="0.0.0.0" --port=5000
