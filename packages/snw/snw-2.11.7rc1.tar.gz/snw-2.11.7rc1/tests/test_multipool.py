import os

import pytest

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt, dt
import connect


# Note: Enable all service before test
# TODO test with 2 services/pools (as previous/first version) instead of only global_pool
def test_goodtask(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    nbtask = len(get_lt(variables["url"], ""))
    taskid_main = get_taskid(
                     launch_train_task(variables["url"], "auto", "systran/pn9",
                                       "0.3", variables['admin_tid'], 1,
                                       service="global_pool"),
                     "ende", variables['admin_tid'])

    status_main = wait_for_status(variables["url"], taskid_main, "stopped", 120)
    assert status_main["message"] == "completed"
    assert status_main["service"] == "global_pool"
    assert len(get_lt(variables["url"], "")) == nbtask + 1
    # assert os.path.isdir(os.path.join("/tmp/taskfiles", taskid_main))
    dt(variables["url"], taskid_main)
    assert not os.path.isdir(os.path.join("/tmp/taskfiles", taskid_main))
    assert len(get_lt(variables["url"], "")) == nbtask
