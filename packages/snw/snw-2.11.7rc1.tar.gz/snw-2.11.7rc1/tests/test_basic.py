import pytest
import requests
import os


@pytest.mark.run(order=1)
def test_api(variables):
    r = requests.get(os.path.join(variables['url'], "status"))
    assert r.status_code == 200
    r = requests.post(os.path.join(variables['url'], "status"))
    assert r.status_code == 405


@pytest.mark.run(order=1)
def test_version(variables):
    r = requests.get(os.path.join(variables['url'], "version"))
    assert r.status_code == 200
    assert len(r.text) > 0 and r.text.find(":") != -1


@pytest.mark.run(order=2)
def test_unknown(variables):
    r = requests.get(os.path.join(variables['url'], "unknown"))
    assert r.status_code == 404
