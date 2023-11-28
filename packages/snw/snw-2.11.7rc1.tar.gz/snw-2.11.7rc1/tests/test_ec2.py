import pytest

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt
import connect


@pytest.mark.online
def test_basic(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskids = get_taskid(
        launch_train_task(variables["url"], "dockersystran", "systran/pn9",
                          "v1.8.0", variables['admin_tid'], 1,
                          service="global_pool", lp="enfr"),
        "enfr", variables['admin_tid'])
    assert len(taskids) == 2, "task should have prepr and train"
    status = wait_for_status(variables["url"], taskids[1], "stopped", 800)
    # it will fail because the configuration is missing vocabulary - but it is not a launch
    # or dependency error
    assert status["message"] == "error"
