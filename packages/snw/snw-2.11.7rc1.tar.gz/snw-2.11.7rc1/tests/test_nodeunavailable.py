import os

import requests
import pytest
import redis

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt
import connect


def test_serverunavailable(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])

    # trainer_david node should be disabled (see conftest)
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 1
    assert lservices["global_pool"]["detail"]["deadlink"]["busy"] != ""

    # let us switch it on
    r = requests.get(os.path.join(variables['url'], "service/enable",
                                  "global_pool", "deadlink"), auth=auth)
    assert r.status_code == 200

    # should be available now
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 0
    assert lservices["global_pool"]["detail"]["deadlink"]["busy"] == ""

    # launch a task that will by default use deadlink (3-GPU), so that work will set deadlink as busy
    # and use another machine to run task correctly
    taskid = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 3, service="global_pool"),
        "ende", variables['admin_tid'])

    # task complete
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"

    # and node was disabled
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 1
    assert lservices["global_pool"]["detail"]["deadlink"]["busy"] != ""

    # check that the disability is temporary
    redis_db = redis.Redis(host=variables["redis_host"],
                           port=variables["redis_port"],
                           db=0,
                           password=variables["redis_password"])
    ttl = redis_db.ttl("busy:global_pool:deadlink")

    assert ttl, "disability should be temporary"
