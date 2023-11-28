import os

import requests
import pytest

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt
import connect


@pytest.mark.skip
def test_binaryfile_issue_9(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    files = {}
    basename = "file.bin"
    files[basename] = (basename, b"\xff\x00\xff\x55")
    config = {
        "source": "en",
        "target": "fr",
        "length": 2,
        "options": {"file": "${TMP_DIR}/%s" % basename}
    }
    taskid = get_taskid(launch_train_task(variables["url"], "auto",
                                          "systran/pn9", "0.3", variables['admin_tid'], 1,
                                          config_json=config,
                                          files=files),
                        "enfr", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"
    r = requests.get(os.path.join(variables["url"], "task/file", taskid, basename), auth=auth)
    assert r.status_code == 200
    assert r.content == b"\xff\x00\xff\x55"


@pytest.mark.skip
def test_binaryfile_issue_50704(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    files = {}
    basename = "f50704.bin"
    with open(os.path.join(str(pytest.config.rootdir), "data", basename), "rb") as f:
        data = f.read()
    files[basename] = (basename, data)
    config = {
        "source": "en",
        "target": "fr",
        "length": 2,
        "options": {"file": "${TMP_DIR}/%s" % basename}
    }
    taskid = get_taskid(launch_train_task(variables["url"], "auto",
                                          "systran/pn9", "0.3", variables['admin_tid'], 1,
                                          config_json=config,
                                          files=files),
                        "enfr", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"
    r = requests.get(os.path.join(variables["url"], "task/file", taskid, basename), auth=auth)
    assert r.status_code == 200
    assert r.content == data


def test_getfile(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "task/file_storage",
                                  "s3_trans", "taskid", "file"), auth=auth)
    assert r.status_code == 400
