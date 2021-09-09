#!/bin/bash
export CLIENT_PORT="9999"
export SERVER_PORT="9999"
export PRODUCTION="TRUE"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR
./student-dashboard.pex backend.main:app  --host 0.0.0.0 --port $SERVER_PORT --ssl-keyfile key.pem --ssl-certfile cert.pem --ssl-keyfile-password hello
