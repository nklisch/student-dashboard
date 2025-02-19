#!/bin/python3
import requests
from datetime import datetime

URL_ROOT = "https://localhost:9999/automation"
api_paths = ["issues", "pulls", "commits", "metrics"]
cookies = {
    "user_id": "",
    "token": "",
}
log = open("daily_log", "a")
for path in api_paths:
    response = requests.request("POST", f"{URL_ROOT}/{path}", cookies=cookies)
    now = datetime.now().ctime()
    if not response.ok:
        log.write(
            f"{now}: {path} failed. Reason: {response.status_code} : {response.reason} - {response.text}.\n"
        )
    else:
        log.write(f"{now}: {path} success.\n")
