# Getting Started

To be able to build this project you will need python 3.8 or greater.

## 1. Check your python version:

```
$ python --version
```

You may have python3 as seperate command:

```
$ python3 --version
```

If you need to update/install python see the following websites: [Ubuntu/Debian](https://docs.python-guide.org/starting/install3/linux/), [CentOS/RedHat](https://www.liquidweb.com/kb/how-to-install-python-3-on-centos-7/)

After you have installed/verified your python installation, verify that the pip command is configured:

```
$ python -m ensurepip --upgrade
```

## 2. Install MariaDB Connector/C 3.1.

This is needed for SQL alchemy mariaDB connector in python.

### 1. Verify you have wget or install it:

Ubuntu

```
$ sudo apt install wget
```

CentOS

```
$ sudo yum install wget
```

### 2. Download the mardiadb_es_repo_setup

```
$ wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
$ chmod +x mariadb_es_repo_setup
```

### 3. Configure the package respoitory:

```
$ sudo ./mariadb_repo_setup \
   --mariadb-server-version="mariadb-10.5"
```

### 4. Install MariaDB

Ubuntu

```
$ sudo apt install libmariadb3 libmariadb-dev
```

CentOS

```
$ sudo yum install MariaDB-shared MariaDB-devel
```

## 3. Create your .env file

You will need to create a _.env_ file in the ./backend folder. A _.env_ file defines environmentail variables. In this case a few of those variables are sensitve, so we will only provide the [template](./CONFIG.md). See Dave/Instructor for the values of the sensitive fields.

## 4. Run the run.sh script

The final step is to run the run.sh script that is in the **deploy-tools** folder

```
$ ./deploy-tools/run.sh
```

This command has three possible parameters: dev, prod and deploy.

Dev installs/checks dependencies and then starts the FastAPI server on port 8000, and npm serves the front end on port 3000. Both the front and backend are hotloaded.

Prod builds the front end and places it in the backend folder under html and the server starts by serving from the python library.

Deploy builds the front and backend and generates a tarball with all the needed dependencies and the run-production.sh script. You can copy this tarball to any machine with python on it and the mariaDB connector and it should work. The cs deparment machines already have the nessicary mariaDB connector, so it will work on those machines and wont require dependencies installation.

# Technologies and Libraries

This list is not exhuastive but it is the main libraries/frameworks that are used in this project.

## Backend

- [FastAPI](https://fastapi.tiangolo.com/) - Backend Framework

- [Poetry](https://python-poetry.org/) - Backend Dependency/Package manager

- [Pydantic](https://pydantic-docs.helpmanual.io/) - Backend Schemas

- [Uvicorn](https://www.uvicorn.org/) - Backend Server

- [Zenhub Connector](https://pypi.org/project/pyzenhub/) - Python

- [Github Connector](https://github.com/PyGithub/PyGithub) - Python

- [SQLAlchemy](https://www.sqlalchemy.org/) - Backend DB connection and Models

- [pex](https://pex.readthedocs.io/en/v2.1.46/) - Deployment packaging tool

- [MariaDB Connector/C](https://mariadb.com/docs/clients/mariadb-connectors/connector-c/install/) - C level DB connector

## Frontend

- [CoreUI 4.0 - Github](https://github.com/coreui/coreui-free-react-admin-template#installation) - Website Template and React component Library

- [CoreUI 4.0 - Documentation](https://coreui.io/react/docs/4.0/getting-started/introduction/)

- [React](https://reactjs.org/) - Frontend framework

- [React Router](https://reactrouter.com/) - Frontend Component for react url paths

- [npm](https://docs.npmjs.com/) - Frontend Dependency/package and build manager

# Deployment

To deploy this project, run the **./deploy-tools/run.sh** with the parameter **"deploy"**.

```
$ ./deploy-tools/run.sh deploy
```

This will create a tarbal called **student-dashboard.tar.gz**. You can copy this tarball over to the desitination computer with scp. The following command will copy the tarball to black-bottle to the student-dashboard on the cs314 user home folder.

```
$ scp student-dashboard.tar.gz cs314@black-bottle.cs.colostate.edu:~/student-dashboard
```

Once copied, ssh into black-bottle and then you can untar the contents with:

```
$ tar -xzf student-dashboard.tar.gz .
```

Once untared, start a [tmux](https://tmuxcheatsheet.com/) session named student-dashboard with -

```
$ tmux new -s student-dashboard
```

Then run **./run-production.sh** script to start the server.

```
$ ./run-production.sh
```

You should see something like the following:

```
INFO:     Started server process [1627092]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9999 (Press CTRL+C to quit)
```

Now detach from the tmux session with _ctrl+b_, then _d_.
Now the server is all setup!

All that is left is to configure a [semester](./CONFIG.md#semester) through the dashboard and setup the [cronjobs](./CONFIG.md#cronjob).

_Note: You can reattach to the tmux session to check on the server status with the following command_:

```
$ tmux a -t student-dashboard
```
