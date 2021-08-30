 #!/bin/bash


function usage {
  echo "usage: $0 [dev/prod/deploy]";
  echo "Default is $0 dev. Prod is a production like environment, but not exactly";
  echo "Deploy creates a tarball that can be untared and used to lauch the apps"
  echo "Options:"
  echo "    -h, --help     :  Display this menu";
  echo ""
}

function check_db_connection {
  DB_CONNECTION=$(ps l | grep faure.cs.colostate.edu | grep -v grep)
  DB_CONNECTION=${DB_CONNECTION// /}
  DOMAINNAME=$(domainname)
  if [ -z $DB_CONNECTION ] && [ $DOMAINNAME != 'cs.colostate.edu' ]; then
    echo "You do not have a tunnel setup to the cs department machines."
    echo "Please run connectdb command."
    exit 1
  fi
}


function check_server_dependencies {
  pushd ./backend > /dev/null
  #!/bin/bash
  POETRY=`pip list | grep poetry`
  if [[ -z POETRY ]]; then
      pip install poetry
  fi
  poetry install
  poetry update --lock
  popd > /dev/null
}

function check_client_dependencies {
  npm install --prefix ./frontend
}

function run_dev {
	echo "Building and Starting the Server in DEVELOPMENT Mode."
	echo
  export CLIENT_PORT="3000"
  export SERVER_PORT="8000"
  check_db_connection
  check_server_dependencies
  check_client_dependencies
  npm --prefix ./frontend run devRun
}

function run_prod {
	echo "Building and Starting the Server in PRODUCTION Mode."
  # npm --prefix ./frontend run build
  # cp -r ./frontend/build/* ./backend/backend/html/
  # docker-compose -f ./deploy-tools/docker-compose.yml up --force-recreate --build
  export CLIENT_PORT="9999"
  export SERVER_PORT="9999"
  check_db_connection
  check_server_dependencies
  rm -r ./frontend/build
  npm --prefix ./frontend run build
  cp -r ./frontend/build/* ./backend/backend/html/
  pushd ./backend > /dev/null
  ./start-server.sh
}

function deploy {
  echo "Building and creating a tar for deployment"
  rm -r ./build
  rm -r ./frontend/build
  export CLIENT_PORT="9999"
  export SERVER_PORT="9999"
  check_server_dependencies
  check_client_dependencies
  npm --prefix ./frontend run build
  mkdir build
  mkdir ./build/backend
  mkdir ./build/backend/html
  cp -r ./frontend/build/* ./build/backend/html
  cd backend
  poetry export -f requirements.txt --output requirements.txt
  poetry run pex --sources-directory=.  -r requirements.txt --script=uvicorn -o ../build/student-dashboard.pex
  cd ..
  cp ./deploy-tools/run-production.sh ./backend/.env ./deploy-tools/dailys.py ./deploy-tools/cron.daily ./build
  cd build
  tar -czf ../student-dashboard.tar.gz . 
}

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}";
}


function get_repo_root_dir {
  dir="$(realpath $1)";
  while [[ ! -d "$dir/.git" ]];
  do
    dir=`echo $dir | sed 's~\(.*\)/.*~\1~'`;
  done;

  export REPO_ROOT=$dir;
}

get_repo_root_dir
cd $REPO_ROOT
PARAMS=""

while (( "$#" )); do
  case "$1" in
    -h|--help)
      usage;
      exit 0;
      ;;
    -d|--deploy)
        deploy
        exit 0
      ;;
    -*|--*=) # unsupported flags
      echo "unrecognized option -- $(echo $1 | sed 's~^-*~~')" >&2
      usage;
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

eval set -- "$PARAMS";

if [[ $1 = "prod" ]]; then
  run_prod
elif [[ $1 = "deploy" ]]; then
  deploy
else
  run_dev
fi