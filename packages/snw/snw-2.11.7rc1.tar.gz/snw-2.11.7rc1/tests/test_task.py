import time
import os
import re
from collections import Counter

import requests
import pytest

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt
import connect


def test_wrongtasks(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    # launch task with wrong image
    taskid = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn8",
                          "0.3", variables['admin_tid'], 1),
        "ende", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "error", "wrong image does not produce launch error"


def test_wrongtasks_size(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    # launch tasks with too many gpus
    message = launch_train_task(variables["url"], "auto", "systran/pn9",
                                "0.3", variables['admin_tid'], 9, expected_statuscode=400)
    # launch tasks with too many cpus
    message = launch_train_task(variables["url"], "auto", "systran/pn9",
                                "0.3", variables['admin_tid'], 1, ncpus=24, expected_statuscode=400)


def test_unknowntask(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "task/status", "SAZZZ_xyyx_UnknownTask"),
                     auth=auth)
    assert r.status_code == 404


@pytest.mark.run(after='test_wrongtasks')
def test_taskenvvarspecific(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskid = get_taskid(
        launch_train_task(variables["url"], "dockersystran", "pn9/testcputest",
                          "0.3", 'SAJAS', 0,
                          service="global_pool"),
        "ende", 'SAJAS')
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"


@pytest.mark.run(after='test_wrongtasks')
def test_nogpu(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    # Cannot run GPU tasks on cpu_server_pool
    launch_train_task(variables["url"], "auto", "systran/pn9",
                      "0.3", variables['admin_tid'], 1, name="GpuCpuTask",
                      service="saling_cputest_pool", expected_statuscode=400)
    taskid = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 0, name="CpuTask",
                          service="global_pool"),
        "ende", variables['admin_tid'])

    status_map = Counter()
    time_spent = 0
    firstCheckRunning = True
    while time_spent < 100:
        lt = get_lt(variables['url'], '%s_ende_CpuTask' % variables['admin_tid'])
        r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
        assert r.status_code == 200
        lservices = r.json()
        for t in lt:
            if t['task_id'] == taskid:
                status_map[t['status']] += 1
                if t['status'] == 'stopped':
                    assert t['message'] == 'completed', "task did not completed"
                    return
                if firstCheckRunning and t['status'] == 'running':
                    # only check service usage for running once
                    firstCheck = False
                    # check that it is actually using 2 cpus
                    assert lservices['global_pool']['usage'] == '0 (2)'
                    # check that the task is showing in ls -v
                    # assert len(lservices['saling_cputest_pool']['detail']['piratus']['usage']) > 0
        time.sleep(1)
        time_spent += 1

    assert False, "test did not complete within %ss" % time_spent


@pytest.mark.run(after='test_wrongtasks')
def test_cpualloc(variables):
    # test that CPU is allocated on the server with most available cpus
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskid_gpu = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 1, service="global_pool"),
        "ende", variables['admin_tid'])
    taskid_cpu = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 0, service="global_pool"),
        "ende", variables['admin_tid'])

    status = wait_for_status(variables["url"], taskid_gpu, "stopped", 120)
    assert status["message"] == "completed"
    status = wait_for_status(variables["url"], taskid_cpu, "stopped", 120)
    assert status["message"] == "completed"

    lt_gpu = get_lt(variables["url"], taskid_gpu)
    assert len(lt_gpu) == 1
    # for gpu optimization, gpu task is launched on david
    assert lt_gpu[0]["alloc_resource"] == "david"
    # for cpu optimization, cpu task is launched on server with largest cpu available
    # that has to be goliath
    lt_cpu = get_lt(variables["url"], taskid_cpu)
    assert len(lt_cpu) == 1
    assert lt_cpu[0]["alloc_resource"] == "goliath"

    taskid_gpu = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 3, service="global_pool"),
        "ende", variables['admin_tid'])
    taskid_cpu = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 0, service="global_pool"),
        "ende", variables['admin_tid'])

    status = wait_for_status(variables["url"], taskid_gpu, "stopped", 120)
    assert status["message"] == "completed"
    status = wait_for_status(variables["url"], taskid_cpu, "stopped", 120)
    assert status["message"] == "completed"

    lt_gpu = get_lt(variables["url"], taskid_gpu)
    assert len(lt_gpu) == 1
    # gpu task can only be launched on goliath since it uses 3 GPU
    assert lt_gpu[0]["alloc_resource"] == "goliath"
    # for cpu optimization, cpu task is launched on server with largest cpu available
    # that has to be goliath
    lt_cpu = get_lt(variables["url"], taskid_cpu)
    assert len(lt_cpu) == 1
    assert lt_cpu[0]["alloc_resource"] == "goliath"


@pytest.mark.run(after='test_wrongtasks')
def test_ntasks(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskid1 = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.1", variables['admin_tid'], 1),
        "ende", variables['admin_tid'])
    taskid2 = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.2", variables['admin_tid'], 2),
        "ende", variables['admin_tid'])
    taskid3 = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 3),
        "ende", variables['admin_tid'])
    taskid4 = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.4", variables['admin_tid'], 4),
        "ende", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid1, "stopped", 120)
    assert status["message"] == "completed"
    lt1 = get_lt(variables["url"], taskid1)
    assert len(lt1) == 1
    assert lt1[0]["alloc_resource"] == "david"
    assert len(lt1[0]["alloc_lgpu"]) == 1

    status = wait_for_status(variables["url"], taskid2, "stopped", 120)
    assert status["message"] == "completed"
    lt2 = get_lt(variables["url"], taskid2)
    assert len(lt2) == 1
    assert len(lt2[0]["alloc_lgpu"]) == 2

    status = wait_for_status(variables["url"], taskid3, "stopped", 120)
    assert status["message"] == "completed"
    lt3 = get_lt(variables["url"], taskid3)
    assert len(lt3) == 1
    assert len(lt3[0]["alloc_lgpu"]) == 3

    status = wait_for_status(variables["url"], taskid4, "stopped", 120)
    assert status["message"] == "completed"
    lt4 = get_lt(variables["url"], taskid4)
    assert len(lt4) == 1
    assert len(lt4[0]["alloc_lgpu"]) == 4


@pytest.mark.run(after='test_wrongtasks')
def test_terminate_tasks(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskids = []
    for i in range(10):
        taskid = get_taskid(
            launch_train_task(variables["url"], "auto", "systran/pn9",
                              "0.1", variables['admin_tid'], 1, name="TermTask"),
            "ende", variables['admin_tid'])
        assert taskid.find("_TermTask_") != -1
        taskids.append(taskid)

    time.sleep(10)
    for taskid in taskids:
        terminate(variables["url"], taskid)

    status_count = Counter()
    for taskid in taskids:
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
        status_count[status["message"]] += 1

    print(status_count)
    assert status_count["aborted"] > 0
    assert status_count["completed"] > 0
    assert len(status_count) == 2


@pytest.mark.run(after='test_wrongtasks')
def test_task_iteration(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskids = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.5", variables['admin_tid'], 1, name="IterTask", iterations=3))

    assert len(taskids) == 3

    idx = 1
    stopped_time = 0
    for taskid in taskids:
        assert taskid.find("_IterTask_0%d_" % idx) != -1
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
        assert status["message"] == "completed", \
            "task %s did not complete" % ("_IterTask_0%d_" % idx)
        # check that the tasks are started after the previous one stop
        assert float(status["allocated_time"]) >= stopped_time
        stopped_time = float(status["stopped_time"])
        idx += 1


@pytest.mark.run(after='test_wrongtasks')
def test_task_iterationerror(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskids = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn",
                          "0.5", variables['admin_tid'], 1, name="IterTaskError", iterations=3))

    assert len(taskids) == 3

    idx = 1
    for taskid in taskids:
        assert taskid.find("_IterTaskError_0%d_" % idx) != -1
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
        assert status["message"] == "error" or "dependency_error"
        # if idx == 1:
        #     assert status["message"] == "launch_error"
        # else:
        #     assert status["message"] == "dependency_error"
        idx += 1


@pytest.mark.run(after='test_wrongtasks')
def test_task_iterationterm(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskids = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.5", variables['admin_tid'], 1, name="IterTaskTerm", iterations=3))

    assert len(taskids) == 3
    terminate(variables["url"], taskids[1])

    idx = 1
    for taskid in taskids:
        assert taskid.find("_IterTaskTerm_0%d_" % idx) != -1
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
        if idx == 1:
            assert status["message"] == "completed"
        elif idx == 2:
            assert status["message"] == "aborted"
        else:
            assert status["message"] == "dependency_error"
        idx += 1


@pytest.mark.run(after='test_wrongtasks')
def test_task_prepr(variables):
    connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskids = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9", "v1.5.0", variables['admin_tid'], 1,
                          name="TaskPrepTrain", iterations=2, resource="goliath"))

    assert len(taskids) == 4
    assert re.search(r"TaskPrepTrain_01_.*_preprocess$", taskids[0]), \
        "invalid task name: %s" % taskids[0]
    assert re.search(r"TaskPrepTrain_01_[^_]*$", taskids[1]), \
        "invalid task name: %s" % taskids[1]
    assert re.search(r"TaskPrepTrain_02_.*_preprocess$", taskids[2]), \
        "invalid task name: %s" % taskids[2]
    assert re.search(r"TaskPrepTrain_02_[^_]*$", taskids[3]), \
        "invalid task name: %s" % taskids[3]
    for taskid in taskids:
        status = wait_for_status(variables["url"], taskid, "stopped", 120)
        assert status["message"] == "completed"


@pytest.mark.run(after='test_wrongtasks')
def test_task_reservation(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])

    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    print("initial service status", lservices)
    assert lservices['global_pool']['detail']["goliath"]['avail_gpus'] == 4
    assert lservices['global_pool']['detail']["goliath"]['avail_cpus'] == 8

    # tasks will be mixing alterning on Goliath necessarily creating allocating states
    taskids1 = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.5", variables['admin_tid'], 3, name="ResIterTask3", iterations=3))
    taskidsb = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.5", variables['admin_tid'], 4, name="ResBlock", iterations=3))

    status_map_1 = Counter()
    status_map_b = Counter()
    count_completed = 0
    time_spent = 0
    while time_spent < 200 and len(taskids1) + len(taskidsb) > 0:
        lt = get_lt(variables['url'], '%s_ende_Res' % variables['admin_tid'])
        for t in lt:
            if len(taskids1) and t['task_id'] == taskids1[0]:
                status_map_1[t['status']] += 1
                if t['status'] == 'stopped':
                    if t['message'] == 'completed':
                        count_completed += 1
                    taskids1.pop(0)
            if len(taskidsb) and t['task_id'] == taskidsb[0]:
                status_map_b[t['status']] += 1
                if t['status'] == 'stopped':
                    if t['message'] == 'completed':
                        count_completed += 1
                    taskidsb.pop(0)
        time.sleep(1)
        time_spent += 1
    assert count_completed == 6, "all tasks did not get completed in %ds" % time_spent
    print("status map for task1", status_map_1)
    print("status map for taskb", status_map_b)
    # TODO make tests to simulate "queued" state
    # assert status_map_1['queued'] == 0, "no queued state for task1"
    # assert status_map_b['queued'] > 0, "some queued state for taskb"

    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    print("final service status", lservices)
    assert lservices['global_pool']['detail']["goliath"]['avail_gpus'] == 4
    assert lservices['global_pool']['detail']["goliath"]['avail_cpus'] == 8


# @pytest.mark.usefixtures("teardown_db")
@pytest.mark.skip
def test_access_task_list_by_role(helper):
    """
     TEST: test_permission_svc_by_user_profile
     GOAL: call service list command with different user role

    """

    # prepare test data
    permissions = helper.get_permissions()
    train_role_id = 2
    trainer_permission = next(item for item in permissions if item['name'] == 'train')
    airfrance_data = helper.add_entity(
        {"name": "airfrance", "entity_code": "AF", "email": "a@airfrance.fr"})

    airbus_entity_id = 3

    airbus_trainer_role = helper.add_role({"name": "airbus_trainer", "entity_id": airbus_entity_id,
                                           "permissions": [
                                               {"permission": trainer_permission["id"]}]})
    airbus_data = helper.get_entity(airbus_entity_id)

    kfc_data = helper.add_entity({"name": "kfc", "entity_code": "KF", "email": "a@kfc.fr"})

    kfc_trainer_role = helper.add_role({'name': 'bnp_trainer', 'entity_id': kfc_data['id'],
                                        'permissions': [{'permission': trainer_permission['id']}]})

    helper.share_role(airbus_trainer_role, airbus_data, airfrance_data)
    helper.share_role(kfc_trainer_role, kfc_data, airfrance_data)
    # check share ok

    roles = helper.get_roles()
    next(item for item in roles if
         item['name'] == "airbus_trainer" and item['entity_id'] == airbus_data['id'])

    next(item for item in roles if
         item['name'] == "bnp_trainer" and item['entity_id'] == kfc_data['id'])

    user_aifrance_data = {
        'first_name': 'coucou',
        'last_name': 'belmondo',
        'email': 'coco.belmondo@systran.fr',
        'password': '0123456789',
        'user_code': 'COC',
        'entity_id': airfrance_data['id']
    }

    # Systran create the new role to use the Airbus share role

    AF_use_sharings_role = {'name': 'af_use_aribus_perm', 'entity_id': airfrance_data['id'],
                            'permissions': [{'permission': trainer_permission['id'],
                                             'entity': airbus_entity_id},
                                            {'permission': trainer_permission['id'],
                                             'entity': kfc_data['id']}]}

    AF_use_sharing_role_created = helper.add_role(AF_use_sharings_role)

    # create the AirFrance user
    coco_user_id = helper.post("user/add", user_aifrance_data)

    user_aifrance_data['roles'] = [train_role_id, AF_use_sharing_role_created['id']]
    user_aifrance_data['user_id'] = coco_user_id

    helper.modify_users(user_aifrance_data)

    # coco_user_AF_created = helper.get('/user/' + str(coco_user_id) + '?detail=True')

    # Now let start the actual test
    # login with the newly user and try ti get the task list

    helper.set_user(user_aifrance_data['email'], user_aifrance_data['password'])
    all_services_list = helper.get("task/list/A*model*")
    all_services_list = helper.get("task/list/*Fmodel*")  # all taches airFrance + KFC: AF + KF
    all_services_list = helper.get("task/list/*Zmodel*")  # all taches airFrance + KFC: AF + KF
    all_services_list = helper.get("task/list/*Fimpossible*")  # all taches airFrance + KFC: AF + KF


@pytest.mark.run(after='test_wrongtasks')
def test_goodtask(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    taskid = get_taskid(
        launch_train_task(variables["url"], "auto", "systran/pn9",
                          "0.3", variables['admin_tid'], 1),
        "ende", variables['admin_tid'])
    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"

    # check status without parameters
    r = requests.get(os.path.join(variables['url'], "task/status", taskid),
                     auth=auth)
    assert r.status_code == 200
    assert 'files' in r.json()

    dirpath = os.path.join(str(pytest.config.rootdir), "models", taskid)
    assert os.path.isdir(dirpath), "cannot find model directory"
    filepath = os.path.join(str(pytest.config.rootdir), "models", taskid, "config.json")
    assert os.path.isfile(filepath), "cannot find configuration file in the model"
