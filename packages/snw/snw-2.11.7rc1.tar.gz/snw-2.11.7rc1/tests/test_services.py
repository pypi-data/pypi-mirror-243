import pytest
import requests
import os
import six
import time
from requests.auth import HTTPBasicAuth
from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt

import connect


def test_ls_minimal(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth, params={"minimal": True})
    assert r.status_code == 200
    lservices = r.json()
    assert len(lservices) == 3
    assert 'saling_test_pool' in lservices and \
           'capacity' not in lservices['saling_test_pool']
    assert 'saling_cputest_pool' in lservices and \
           'capacity' not in lservices['saling_cputest_pool']
    assert 'global_pool' in lservices and \
           'capacity' not in lservices['global_pool']


def test_ls(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert len(lservices) == 3
    assert 'saling_test_pool' in lservices and \
           lservices['saling_test_pool']['capacity'] == "8 (20)"
    assert 'saling_cputest_pool' in lservices and \
           lservices['saling_cputest_pool']['capacity'] == "0 (8)"
    assert 'global_pool' in lservices and \
           lservices['global_pool']['capacity'] == "9 (22)"
    assert lservices['saling_test_pool']["busy"] == 1
    assert lservices['saling_cputest_pool']["busy"] == 0


@pytest.mark.run(after='test_ls')
def test_check(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/check", "saling_test_pool"),
                     json={"server": "goliath"}, auth=auth)
    assert r.status_code == 200
    result = r.json()
    assert "gpus" in result and len(result["gpus"]) == 4
    assert "disk" in result


@pytest.mark.run(after='test_ls')
def test_check_unavailable(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/check", "saling_cputest_pool"),
                     json={"server": "cpu_server_01:2223"}, auth=auth)
    assert r.status_code == 500


@pytest.mark.run(after='test_ls')
def test_describe(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/describe", "saling_test_pool"),
                     auth=auth)
    assert r.status_code == 200
    result = r.json()
    assert len(result["server"]["enum"]) == 9


@pytest.mark.run(after='test_ls')
def test_disable(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices['saling_test_pool']['busy'] == 1
    assert lservices['saling_test_pool']['detail']['deadlink']['busy']
    r = requests.get(os.path.join(variables['url'], "service/disable",
                                  "saling_test_pool", "goliath"), auth=auth)
    assert r.status_code == 200
    result = r.json()
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices['saling_test_pool']['busy'] == 2
    assert lservices['saling_test_pool']['detail']['goliath']['busy'] == 'DISABLED'
    r = requests.get(os.path.join(variables['url'], "service/enable",
                                  "saling_test_pool", "goliath"), auth=auth)
    assert r.status_code == 200
    result = r.json()
    r = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r.status_code == 200
    lservices = r.json()
    assert lservices['saling_test_pool']['busy'] == 1
    assert lservices['saling_test_pool']['detail']['goliath']['busy'] == ''


@pytest.mark.skip
def test_restart(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'], variables['admin_password'])
    taskid = get_taskid(
        launch_train_task(variables["url"], "dockersystran", "systran/pn9",
                          "0.3", variables['admin_tid'], 1, service="saling_test_pool", duration=30),
        "ende", variables['admin_tid'])

    status = wait_for_status(variables["url"], taskid, "running", 20)

    # that a snapshot of current tasks running
    r_ref = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r_ref.status_code == 200

    ls_ref = r_ref.json()["saling_test_pool"]

    # restart the service in the meantime
    r = requests.get(os.path.join(variables['url'], "service/restart", "saling_test_pool"),
                     auth=auth)
    assert r.status_code == 200

    # wait for the worker to be up and fully restart
    time.sleep(5)

    # check that the tasks running is still the same (no loss of cpu count)
    r_now = requests.get(os.path.join(variables['url'], "service/list"), auth=auth)
    assert r_now.status_code == 200

    ls_now = r_now.json()["saling_test_pool"]

    assert ls_ref["pid"] != ls_now["pid"], "pid of worker should have changed"
    ls_ref["pid"] = None
    ls_now["pid"] = None

    # assert ls_ref == ls_now, "task details should not have changed at restart"

    status = wait_for_status(variables["url"], taskid, "stopped", 120)
    assert status["message"] == "completed"


"""
 TEST: test_permission_svc_by_user_profil
 GOAL: call service list command with different user role

"""


@pytest.mark.skip
@pytest.mark.usefixtures("teardown_db")
def test_access_svc_list_by_role(helper):
    trainer_role = next(item for item in helper.get_roles() if item['name'] == 'trainer')
    user_role = next(item for item in helper.get_roles() if item['name'] == 'user')

    # super admin see services of all entities
    all_services_list = helper.get("service/list?all=True")
    assert all_services_list

    entities_seen_by_super_admin = [e[:2] for e in all_services_list.keys()]
    assert 'so' in entities_seen_by_super_admin  # entity SO
    assert 'sa' in entities_seen_by_super_admin

    # trainer can see only his entity
    data = {
        'first_name': 'coco',
        'last_name': 'belmondo',
        'email': 'coco.belmondo@systran.fr',
        'password': '0123456789',
        'user_code': 'COC'
    }

    # TEST: create the user
    coco_user_id = helper.post("user/add", data)

    data['roles'] = [trainer_role['id']]
    data['user_id'] = coco_user_id
    helper.modify_users(data)

    helper.set_user(data['email'], data['password'])
    services_seen_by_trainer = helper.get("service/list")

    assert services_seen_by_trainer

    entities_seen_by_trainer = [e[:2] for e in services_seen_by_trainer.keys()]

    assert 'so' not in entities_seen_by_trainer  # entity SO
    assert 'sa' in entities_seen_by_trainer

    # a user cannot see any service
    helper.set_defaut_user()  # relogin as admin to changer the role of the user
    data['roles'] = [user_role['id']]
    helper.modify_users(data)

    helper.set_user(data['email'], data['password'])

    services_seen_by_user = helper.get("service/list")

    assert len(services_seen_by_user) == 0
