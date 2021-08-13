#!/bin/bash


curl -L -b cookie.txt \
	-X POST \
	-d '{"get_response_body": "false"}' \
	http:/localhost:8000/automation/commits?start_date=2021-04-13T15:38:32.760Z&end_date=2021-04-25T15:38:32.760Z