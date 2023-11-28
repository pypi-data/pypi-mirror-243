import os

import pytest
import requests
import redis

import connect
from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt


def test_maxlogsize(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    config = {
        "source": "en",
        "target": "fr",
        "length": 2,
        "options": {"buffer": "x" * 100000}
    }
    taskid = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 1, config_json=config),
        "enfr", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid, "stopped", 120)

    assert status["message"] == "completed"

    # TODO check how to make it work with current mode of Gitlab-ci, this is only work for local mode
    # filepath = os.path.join(variables["tmp_dir"], taskid, "log")
    # assert os.path.isfile(filepath), "cannot find log file (%s)" % filepath
    # current_size = os.stat(filepath).st_size
    # assert current_size == 100000, "log file did not get truncated"


# test restart of service - during training
def test_servicerestart(variables):
    redis_db = redis.Redis(host=variables["redis_host"],
                           port=variables["redis_port"],
                           db=0,
                           password=variables["redis_password"])
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskids = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 1, iterations=2,
                          name="ServiceRestart", service="global_pool"),
        "ende", variables['admin_tid'])

    r = requests.get(os.path.join(variables["url"], "service/restart", "global_pool"),
                     auth=auth)
    assert r.status_code == 200
    assert r.json() == "ok"

    idx = 1
    for taskid in taskids:
        assert taskid.find("_ServiceRestart_0%d_" % idx) != -1
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
        assert status["message"] == "completed", \
            "task %s did not complete" % ("_ServiceRestart_0%d_" % idx)
        idx += 1

    # check that no noise has been introduced in redis at task restart
    redis_db = redis.Redis(host=variables["redis_host"],
                           port=variables["redis_port"],
                           db=0,
                           password=variables["redis_password"])
    assert not redis_db.exists(taskids[0]), "corrupted database - taskid without task: prefix"
