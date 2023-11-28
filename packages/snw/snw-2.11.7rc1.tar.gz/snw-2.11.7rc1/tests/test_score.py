import os

import pytest
import requests

from util_task import get_taskid, wait_for_status, launch_train_task
import connect


@pytest.mark.skip
def test_fullseqchain(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    content = {
        "toscore": [["pn9_testtrans:<MODEL>/en_fr/test-3.en.fr", "pn9_testing:en_fr/test-3.fr"],
                    ["pn9_testtrans:<MODEL>/en_fr/test-2.en.fr", "pn9_testing:en_fr/test-2.fr"],
                    ["pn9_testtrans:<MODEL>/en_fr/test-5.en.fr", "pn9_testing:en_fr/test-5.fr"],
                    ["pn9_testtrans:<MODEL>/en_fr/test-1.en.fr", "pn9_testing:en_fr/test-1.fr"],
                    ["pn9_testtrans:<MODEL>/en_fr/test-4.en.fr", "pn9_testing:en_fr/test-4.fr"]],
        "totranslate": [["pn9_testing:en_fr/test-3.en", "pn9_testtrans:<MODEL>/en_fr/test-3.en.fr"],
                        ["pn9_testing:en_fr/test-2.en", "pn9_testtrans:<MODEL>/en_fr/test-2.en.fr"],
                        ["pn9_testing:en_fr/test-5.en", "pn9_testtrans:<MODEL>/en_fr/test-5.en.fr"],
                        ["pn9_testing:en_fr/test-1.en", "pn9_testtrans:<MODEL>/en_fr/test-1.en.fr"],
                        ["pn9_testing:en_fr/test-4.en", "pn9_testtrans:<MODEL>/en_fr/test-4.en.fr"]],
        "docker": {"command": ["-c", "{\"source\": \"en\", \"data\": {\"sample\": 50, "
                                     "\"train_dir\": \"en_fr\""", "
                                     "\"sample_dist\": [{\"path\": \"train\", \"distribution\": "
                                     "[[\"*\", 1]]}]}, \""
                               "target\": \"fr\", \"options\": {\"duration\": 5}}",
                               "train"],
                   "registry": "auto"},
        "wait_after_launch": 2,
        "options": {}}
    taskids = get_taskid(
                launch_train_task(variables["url"], "auto", "systran/pn9_tf",
                                  "v1.13.0", 'SAJAS', 1,
                                  content=content, push=True),
                "enfr", 'SAJAS')
    assert len(taskids) == 4, "not all tasks have been launched"
    status = wait_for_status(variables["url"], taskids[3], "stopped", 200)
    assert status["message"] == "completed"

    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"model": taskids[1], "source": "en", "target": "fr", "scores": ""},
                     auth=auth)
    print(r.json())
    assert r.status_code == 200
    assert isinstance(r.json(), list) and len(r.json()) == 1
    model = r.json()[0]
    assert "scores" in model and "en_fr/test-5" in model["scores"]
    # ATTENTION => break old format of MongoDB=>models=>score/test
    assert len(model["scores"]["en_fr/test-5"]["score"]) >= 6
