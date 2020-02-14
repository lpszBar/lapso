
#! /bin/sh

set -o errexit
set -o nounset 

main(){
    echo "Checking if db is ready..."

    if [ ! -s lapso.db ]; then
        echo "Lapso db does not exist. Creating it..."
        sqlite3 lapso.db < lapso.schema
        echo "Lapso db created 🏗"
    else
        echo "Lapso db ✅"
    fi
}

main
