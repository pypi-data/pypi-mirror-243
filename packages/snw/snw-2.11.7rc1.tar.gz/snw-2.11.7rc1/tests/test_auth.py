import os
import time
import sys
import requests
import pytest
import json
from requests.auth import HTTPBasicAuth

import connect


@pytest.mark.run(order=3)
def test_auth(variables):
    r = requests.get(os.path.join(variables['url'], "user/list"))
    # sys.stdout.write(str(r.status_code))
    # sys.stdout.write(json.dumps(r.json()))
    assert not isinstance(r, list)
    try:
        auth = connect.get_token(False, variables['url'], 'nobody', 'nopassword')
    except AssertionError as e:
        pass
    auth = connect.get_token(False, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 200
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "user/list?detail=True"), auth=auth)
    assert r.status_code == 200
    lusers = r.json()
    # sys.stdout.write(str(r.status_code))
    # sys.stdout.write(json.dumps(r.json()))
    assert len(lusers) >= 45, "there should be 1 user at test initialization"

    assert lusers[0].get('id'), "missing id field in list user"
    assert 'SA' in lusers[0]['entity_code'], "user must be in Systran entity"
    assert 'admin' in map(lambda roles: roles['name'],
                          lusers[0]['roles']), "user should have 'super' role"


@pytest.mark.run(order=4)
# @pytest.mark.skip
def test_logout(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "auth/revoke"), auth=auth,
                     params={'token': auth.username})
    assert r.status_code == 200
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 401

    auth = connect.get_token(False, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert not isinstance(r, list)


@pytest.mark.run(order=4)
# @pytest.mark.skip
def test_persistent(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    assert auth.username.startswith("_T_")
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'], True)
    assert auth.username.startswith("_P_")
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 200


@pytest.mark.run(order=4)
# @pytest.mark.skip
def test_duration(variables):
    auth = connect.get_token(False, variables['url'], variables['admin_user'],
                             variables['admin_password'],
                             duration=3)
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 200
    time.sleep(5)
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 401


@pytest.mark.run(order=5)
# @pytest.mark.skip
def test_existingtoken(variables):
    auth = HTTPBasicAuth('_T_eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4NjQwNjY0NCwiZXhwIjoxNTg3MDExNDQ0fQ.eyJ'
                         'pZCI6MX0.O2xH6MB8ZnEKmSnKa5X0OIvQtmzGWbNPD6du5vNitUJl3qCR5aii5Cz0_N7j-TqE'
                         'wBuIZz75ulfJ7V0KJffmZg', 'x')
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 401
    auth = HTTPBasicAuth("_P_KKAhbGciOiJIUzUxMiIsImV4cCI6MTU0NDM4NTEyMSwiaWF0Ij"
                         "oxNTQzMzg1MTIxfQ.eyJpZCI6MX0.NQ5w9fnMlwCPnotzYe6va9m7"
                         "QysGnE9TpCxIMT__azoDjUkyZlP4NiYUb1Ze76Kcm4PsvEOThSkef"
                         "-3-dUP30w", 'x')
    r = requests.get(os.path.join(variables['url'], "user/list"), auth=auth)
    assert r.status_code == 401
