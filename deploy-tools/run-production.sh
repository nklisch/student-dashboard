#!/bin/bash
export CLIENT_PORT="8000"
export SERVER_PORT="8000"
export PRODUCTION="TRUE"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR
./student-dashboard.pex backend.main:app --port $SERVER_PORT
