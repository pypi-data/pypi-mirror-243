import six

import pytest

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt, \
    check_xpu_alloc
import connect


def test_basic_taskalloc(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskids = []

    # basic task - 1 gpu, default cpu
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "0.3", variables['admin_tid'], 1)
    assert isinstance(launch_result,
                      six.text_type), "with image 0.3 - one iteration should be one task"
    taskid = check_xpu_alloc(variables["url"], launch_result, (1, 2), "train", auth=auth)
    taskids.append(taskid)

    # basic task - 1 gpu, manual cpu setting
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "0.3", variables['admin_tid'], 1, ncpus=3)
    assert isinstance(launch_result,
                      six.text_type), "with image 0.3 - one iteration should be one task"
    taskid = check_xpu_alloc(variables["url"], launch_result, (1, 3), "train", auth=auth)
    taskids.append(taskid)

    # basic task - 0 gpu, manual cpu setting
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "0.3", variables['admin_tid'], 0, ncpus=3)
    assert isinstance(launch_result,
                      six.text_type), "with image 0.3 - one iteration should be one task"
    taskid = check_xpu_alloc(variables["url"], launch_result, (0, 3), "train", auth=auth)
    taskids.append(taskid)

    for taskid in taskids:
        terminate(variables["url"], taskid, auth=auth)

    for taskid in taskids:
        status = wait_for_status(variables["url"], taskid, "stopped", 120)


def test_chainprepr_taskalloc(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskids = []

    # one task with chainprepr
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "v1.4.0", variables['admin_tid'], 1)
    assert isinstance(launch_result, list), "with image 1.4.0 - by default chain prepr"
    assert len(launch_result) == 2
    taskid = check_xpu_alloc(variables["url"], launch_result[0], (0, 4), "prepr", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[1], (1, 2), "train", auth=auth)
    taskids.append(taskid)

    # the same without chainprepr
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "0.3", variables['admin_tid'], 1, nochainprepr=True)
    assert isinstance(launch_result, six.text_type), "with image 1.4.0, nochainprep -" \
                                                     " one iteration should be one task"
    taskid = check_xpu_alloc(variables["url"], launch_result, (1, 2), "train", auth=auth)
    taskids.append(taskid)

    for taskid in taskids:
        terminate(variables["url"], taskid, auth=auth)

    for taskid in taskids:
        status = wait_for_status(variables["url"], taskid, "stopped", 120)


def test_chaintrans_taskalloc(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskids = []

    # one task with chaintrans
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "v0.3.0", variables['admin_tid'], 1,
                                      totranslate=[("a:f.in", "b:f.out"), ("a:g.in", "b:g.out")])
    assert isinstance(launch_result, list)
    assert len(launch_result) == 2
    taskid = check_xpu_alloc(variables["url"], launch_result[0], (1, 2), "train", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[1], (0, 4), "trans", auth=auth)
    taskids.append(taskid)

    # with 2 gpus trans are distributed
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "v0.3.0", variables['admin_tid'], 2,
                                      totranslate=[("a:f.in", "b:f.out"), ("a:g.in", "b:g.out")])
    assert isinstance(launch_result, list)
    assert len(launch_result) == 3
    taskid = check_xpu_alloc(variables["url"], launch_result[0], (2, 2), "train", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[1], (0, 4), "trans", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[2], (0, 4), "trans", auth=auth)
    taskids.append(taskid)

    # with version 1.8.0+ translation by default on cpu
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "v1.8.0", variables['admin_tid'], 2,
                                      totranslate=[("a:f.in", "b:f.out"), ("a:g.in", "b:g.out")],
                                      nochainprepr=True)
    assert isinstance(launch_result, list)
    assert len(launch_result) == 2
    taskid = check_xpu_alloc(variables["url"], launch_result[0], (2, 2), "train", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[1], (0, 4), "trans", auth=auth)
    taskids.append(taskid)

    # with version 1.8.0+ translation by default on cpu, except if notransasrelease is set
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "v1.8.0", variables['admin_tid'], 2,
                                      totranslate=[("a:f.in", "b:f.out"), ("a:g.in", "b:g.out")],
                                      nochainprepr=True, notransasrelease=True)
    assert isinstance(launch_result, list)
    assert len(launch_result) == 3
    taskid = check_xpu_alloc(variables["url"], launch_result[0], (2, 2), "train", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[1], (0, 4), "trans", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[2], (0, 4), "trans", auth=auth)
    taskids.append(taskid)

    # it combines with chainprepr too...
    launch_result = launch_train_task(variables["url"], "auto", "systran/pn9",
                                      "v1.8.0", variables['admin_tid'], 2,
                                      totranslate=[("a:f.in", "b:f.out"), ("a:g.in", "b:g.out")])
    assert isinstance(launch_result, list)
    assert len(launch_result) == 3
    taskid = check_xpu_alloc(variables["url"], launch_result[0], (0, 4), "prepr", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[1], (2, 2), "train", auth=auth)
    taskids.append(taskid)
    taskid = check_xpu_alloc(variables["url"], launch_result[2], (0, 4), "trans", auth=auth)
    taskids.append(taskid)

    for taskid in taskids:
        terminate(variables["url"], taskid, auth=auth)

    for taskid in taskids:
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
