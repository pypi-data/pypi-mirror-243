import os

import requests
import pytest

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt
import connect


def test_freebox(variables):
    assert not os.path.isfile(os.path.join(str(pytest.config.rootdir),
                                           "control",
                                           "david",
                                           "nvidia-smi_output"))

    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/check", "global_pool"),
                     json={"server": "david"},
                     auth=auth)
    assert r.status_code == 200
    res = r.json()
    assert "gpus" in res
    assert res["gpus"][0]["mem"] == 8000
    assert res["gpus"][1]["mem"] == 8000

    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 1


@pytest.mark.run(after='test_freebox')
def test_busybox(variables):
    # variables = global_va
    # put a control file to simulate that the node is busy
    with open(os.path.join(str(pytest.config.rootdir),
                           "control",
                           "david",
                           "nvidia-smi_output"),
              "w") as f:
        f.write("Gpu: 55%%\nFree: 2000 MiB\n")
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/check", "global_pool"),
                     json={"server": "david"},
                     auth=auth)
    assert r.status_code == 200
    res = r.json()
    assert "gpus" in res
    assert res["gpus"][0]["mem"] == 2000
    assert res["gpus"][1]["mem"] == 2000

    # service is still not busy - we need to make a request on it first
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 1


@pytest.mark.run(after='test_busybox')
def test_runtask(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    assert os.path.isfile(os.path.join(str(pytest.config.rootdir),
                                       "control",
                                       "david",
                                       "nvidia-smi_output"))

    taskid = get_taskid(
        launch_train_task(variables["url"], "dockersystran", "systran/pn9",
                          "0.3", variables['admin_tid'], 2),
        "ende", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"
    assert status["alloc_resource"] == "goliath"

    # service is still not busy - we need to make a request on it first
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 2
    assert lservices["global_pool"]["detail"]["david"]["busy"] != ""


@pytest.mark.run(after='test_runtask')
def test_unbusybox(variables):
    os.remove(os.path.join(str(pytest.config.rootdir),
                           "control",
                           "david",
                           "nvidia-smi_output"))
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/enable",
                                  "global_pool", "david"), auth=auth)
    assert r.status_code == 200
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices["global_pool"]["busy"] == 1
