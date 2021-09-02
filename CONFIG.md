# Configuration

## ./backend/.env

```
AUDITS=FALSE                        # This activates auditing requests
DB_DEV_URL=127.0.0.1:3306
DB_PROD_URL=faure:3306
DB_USER=cs314dashboard_admin
DB_PASSWORD=
DB_NAME=cs314dashboard
DB_ENCRYPT_KEY=                     # This is an encryption key for certian fields of the database
GITHUB_KEY=                         # This is the Github API key the backend uses for API requests
ZENHUB_KEY=                         # This is the Zenhub API key the backend uses
GITHUB_CLIENT_ID=                   # This is the unique ID generated for this oauth on github
GITHUB_CLIENT_SECRET=               # This is the secret required to for github Oauth
```

See Dave for these fields via messaging. These wont be checked into source control.

## Configuring Github Oauth

# Setup

Before each semester you must enter some configuration options so that the backend can pull the needed data from github.
Follow these steps:

## Semester

### 1. Go to the deployed student dashboard.

Since you are a TA or Instructor you should have the view of a semester.

- Select the semester and year you want to setup.
- Enter in the exact name of the new github orginization - as it appears in the URL is best.
- Then click "Add Sprint" to add a sprint. Sprints should be directly next to each other in their date ranges.
- Finally, once the semester is started and all the repo for the students have been made and all the student's have been assigned to them, you can click to pull the repo and teams/user data. This will update the database with this information.

The last piece needed for setup is to start the cronjobs.

## Cronjobs
