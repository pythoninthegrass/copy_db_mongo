#!/usr/bin/env bash

set -euo pipefail

# env vars
ENV=$(env | grep -E 'DB_NAME|DB_USER|DB_PASS')
for var in $ENV; do
	export ${var?}
done
DB_NAME="${DB_NAME:-test}"
DB_USER="${DB_USER:-root}"
DB_PASS="${DB_PASS:-toor}"

# check if mongod is already running
check() {
	if [[ -z $(pgrep mongod >/dev/null 2>&1; echo $?) ]]; then
		return 0
	else
		return 1
	fi
}

# stop the mongodb server
stop() {
	if [[ $(check) -eq 1 ]]; then
		echo "Stopping mongod..."
		pkill mongod
	fi
}

# start the mongodb server in background
start() {
	stop
	if [[ $# -eq 1 ]]; then
		case $1 in
			--auth)
				echo "Starting mongod with access control..."
				mongod --bind_ip_all --auth --maxConns 1000 &
				sleep 10
				;;
			--noauth)
				echo "Starting mongod without access control..."
				mongod --bind_ip_all --noauth --maxConns 1000 &
				sleep 10
				;;
			*)
				echo "Invalid argument: $1"
				exit 1
				;;
		esac
	fi
}

# create a javascript file with the commands to create the user
create_user() {
if [[ ! -f "create_user.js" ]]; then
	cat <<-EOF > create_user.js
	use admin
	db.createUser(
	    {
	        user: "${DB_USER}",
	        pwd: "${DB_PASS}",
	        roles: [
	            { role: "root", db: "admin" },
	        ]
	    }
	)
	EOF
fi
	# run the javascript file with the mongo command
	mongosh < create_user.js
}

# create database
create_db() {
	mongosh \
		--username "${DB_USER}" \
		--password "${DB_PASS}" \
		--eval "db = db.getSiblingDB('${DB_NAME}'); db.createCollection('_temp')"
}

# disable telemetry (mongosh --nodb --eval "disableTelemetry()")
disable_telemetry() {
	mongosh --nodb --eval "disableTelemetry()"
}

# remove all databases and collections
reset_db() {
	echo "Dropping all databases and collections..."
	mongosh \
		--username "${DB_USER}" \
		--password "${DB_PASS}" \
        --eval "db.getMongo().getDBNames().forEach(function(database) { if (database !== 'admin') { db.getSiblingDB(database).dropDatabase(); } });"
}

# import the csv files
import_csv() {
	for filename in ./backup/*.csv; do
		collection=$(basename ${filename%.csv})
		mongoimport \
            --authenticationDatabase admin \
			--username "${DB_USER}" \
			--password "${DB_PASS}" \
            --type csv \
			--headerline \
			--file "${filename}" \
			--db "${DB_NAME}" \
			--collection "${collection}" \
			--drop
	done
}

keep_alive() {
	sleep infinity
}

main() {
	start --noauth
	create_user
	start --auth
	disable_telemetry
	reset_db
	import_csv
	keep_alive
}
main "$@"

exit 0
