 #!/bin/bash
function usage {
  echo "usage: $0 [dev/prod]";
  echo "Default is $0 dev";
  echo "Options:"
  echo "    -h, --help     :  Display this menu";
  echo "    -d, --deploy [docker-hub username]  :  Deploy built image to docker hub under your user"
  echo ""
}


function check_client_dependencies {
  if [ ! -d "./frontend/node_modules" ]; then
    # install all dependencies into node_modules
    npm install --prefix ./client
  fi
}

function run_dev {
	echo "Building and Starting the Server in DEVELOPMENT Mode."
	echo
    DOCKER_UP=docker ps | grep postgres;
    if [[ -z $DOCKER_UP ]]; then
      docker-compose -f ./deploy-tools/docker-compose.yml up -d db 
    fi
    check_client_dependencies;
    npm --prefix ./frontend run devRun
}

function run_prod {
	echo "Building and Starting the Server in PRODUCTION Mode."
    npm --prefix ./frontend run build
    cp -r ./frontend/build/* ./backend/backend/html/
    docker-compose -f ./deploy-tools/docker-compose.yml up --force-recreate --build
}

function deploy {
  echo "Building new docker image and pushing it to dockerhub"
  cd ./backend
  IMAGE="$DOCKERHUB_USERNAME/csu-cs314-student-dashboard"
  docker build -t $IMAGE .
  docker push $IMAGE
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
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        DOCKERHUB_USERNAME=$2
        shift 2
        deploy
        exit 0
      else
        echo "argument missing for -- $1" >&2
        exit 1
      fi
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
else
  run_dev
fi
