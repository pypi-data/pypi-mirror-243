import time
from collections import Counter

import requests
import pytest

import os
import re

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt
import connect


@pytest.mark.skip
def test_beatandlog(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskid = get_taskid(
                launch_train_task(variables["url"], "auto", "systran/pn9",
                                  "0.3", variables['admin_tid'], 0,
                                  lp="enfr", duration=250, service="global_pool"),
                "enfr", variables['admin_tid'])

    # check that the task is beating (test parameters is every 100s)
    # and send log every 60 seconds

    allwait = 0
    status = None
    last_updated_time = 0
    count_updated = 0
    last_log = ""
    count_change_log = 0
    while True:
        params = {"fields": "status,updated_time"}
        r = requests.get(os.path.join(variables["url"], "task/status", taskid), auth=auth,
                         params=params)
        assert r.status_code == 200
        status = r.json()
        print("update", status["updated_time"])
        if status["updated_time"] != last_updated_time:
            count_updated += 1
            last_updated_time = status["updated_time"]
        r = requests.get(os.path.join(variables["url"], "task/log", taskid), auth=auth,
                         params=params)
        if r.status_code == 200:
            # log = r.text.encode("utf-8")
            log = r.text
            print("log", log.replace("\n", "\\n")[-80:])
            if log != last_log:
                count_change_log += 1
                last_log = log
        if status["status"] == "stopped":
            break
        time.sleep(5)
        allwait += 5
        if allwait == 140:
            requests.get(os.path.join(variables["url"], "task/terminate", taskid), auth=auth)

    assert allwait < 200, "task should have been stopped at t=140"
    # assert count_updated - count_change_log >= 1, "beat and patch log updates status"
    assert count_change_log >= 2, "log should have at least been changed at t=0, t=60, t=120"
