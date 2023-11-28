import os
import json
import sys
import pytest
import requests
import connect


SERVICE = "global_pool"


def get_config(variables):
    auth = connect.get_authorized(variables)
    r = requests.get(os.path.join(variables['url'], "service/configs", SERVICE), auth=auth)
    return r.json()


def test_get_config(variables):
    auth = connect.get_authorized(variables)
    r = requests.get(os.path.join(variables['url'], "service/configs", SERVICE), auth=auth)
    sys.stdout.write(str(r.status_code))
    sys.stdout.write(json.dumps(r.json()))

    assert r.status_code == 200
    result = r.json()
    assert isinstance(result, dict) and result["name"] == SERVICE


@pytest.mark.run(after='test_get_config')
def test_set_config(variables):
    auth = connect.get_authorized(variables)
    r = requests.post(os.path.join(variables['url'], "service/configs",
                                   SERVICE), data={'config': ""}, auth=auth)
    assert r.status_code == 400
    result = r.json()
    assert result["message"].startswith("Expecting value")

    config = get_config(variables)
    config["name"] = "other_name"
    r = requests.post(os.path.join(variables['url'], "service/configs",
                                   SERVICE), data={'config': json.dumps(config)}, auth=auth)
    assert r.status_code == 200
    config = get_config(variables)
    assert config["name"] == SERVICE
