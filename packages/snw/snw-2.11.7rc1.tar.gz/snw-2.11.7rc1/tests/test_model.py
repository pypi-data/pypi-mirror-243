import os
import json
import gzip

from six import StringIO
import pytest
import requests

from user_helper import UserHelper
import connect

from util_task import get_taskid, wait_for_status, terminate, launch_train_task, get_lt

import sys

# sys.path.append(sys.path[0] + "/../server")
from lib.pn9model import ConcurrentCompanies, PN9Model

SA_models = None


def test_pushmodel(variables):
    auth = connect.get_token(True, variables['url'], 'leidiana.martins@systrangroup.com', '0123456789')
    taskid1 = get_taskid(launch_train_task(variables["url"], "auto", "systran/pn9", "0.3", 'SALMA', 1,
                                           iterations=1, push=False, auth=auth), "ende", 'SALMA')

    taskid2s = get_taskid(launch_train_task(variables["url"], "auto", "systran/pn9", "0.3", 'SALMA', 1,
                                            iterations=2, push=True, auth=auth), "ende", 'SALMA')

    # The 2 tasks must complete
    status1 = wait_for_status(variables["url"], taskid1, "stopped", 120, auth=auth)
    status2 = wait_for_status(variables["url"], taskid2s[1], "stopped", 120, auth=auth)
    assert status1["message"] == "completed"
    assert status2["message"] == "completed"

    # The first one does not have pushed the model
    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"model": taskid1}, auth=auth)
    assert r.status_code == 200
    assert isinstance(r.json(), list) and len(r.json()) == 0

    # But the second task has pushed 2 models
    model2_split = taskid2s[0].split("_")
    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"model": model2_split[2]}, auth=auth)
    assert r.status_code == 200
    assert isinstance(r.json(), list) and len(r.json()) == 2
    global SA_models
    SA_models = taskid2s


@pytest.mark.run(after='test_pushmodel')
def test_getmodel(variables):
    auth = connect.get_token(True, variables['url'], variables['admin_user'],
                             variables['admin_password'])
    # The first one does not have pushed the model
    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"source": "en", "target": "de"}, auth=auth)
    assert r.status_code == 200
    # x = r.json()
    assert isinstance(r.json(), list) and len(r.json()) >= 2, \
        "there should be at least 2 en-de language pair in the catalog"

    res = sorted(r.json(), key=lambda m: m["date"])
    # check model description is ok
    d = res[-1]
    assert isinstance(d, dict)
    assert "model" in d
    assert "lp" in d
    assert "date" in d
    assert "sentenceCount" in d
    assert "imageTag" in d
    assert "cumSentenceCount" in d
    assert "parent_model" in d
    assert d["parent_model"] == res[-2]["model"]

    global SA_models
    assert d["model"] == SA_models[1]
    assert d["parent_model"] == SA_models[0]

    r = requests.get(os.path.join(variables["url"], "model/listfiles", d["model"]),
                     auth=auth)

    res = sorted(r.json())
    assert res == [d["model"] + '/' + f for f in ['checksum.md5', 'config.json', 'model']]

    # The first one does not have pushed the model
    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"source": "xy", "target": "yx"}, auth=auth)
    assert r.status_code == 200
    assert r.json() == [], "should return no model for xy-yx language pair"


@pytest.mark.skip
def test_SA_cannot_delete_model_owned_by_SS(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    SA_trainer = helper.get("user/whoami")
    assert "SA" == SA_trainer["entity_code"]

    model = "SAADM_enfr_testmodel_01_4f1d766bb40e4dc8a-0926e"
    models = helper.get('model/list?detail=False&model=%s' % model)

    assert models and len(models) == 1 and models[0]

    the_model = models[0]
    assert the_model['owner']['entity_code'] == 'SS'

    helper.get("model/delete/en/fr/%s" % model, {"recursive": 1, "dryrun": 1}, 405)


@pytest.mark.run(after='test_delmodel')
def test_addmodel(variables):
    auth = connect.get_token(True, variables['url'], 'admin@systran.fr', 'snwsuperpassword')
    # The first one does not have pushed the model
    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"source": "en", "target": "de"}, auth=auth)
    assert r.status_code == 200

    data_dir = str(pytest.config.rootdir / "data")
    filename = "SAJAS_ende_WahrerKuckuck_01_67733f328b15422c841"
    file = os.path.join(data_dir, filename + ".tgz")

    params = {
        "ignore_parent": True,
        "compute_checksum": True
    }

    r = requests.get(os.path.join(variables["url"], "model/delete",
                                  "en", "de", filename), auth=auth)
    assert r.status_code == 200 or r.status_code == 400, \
        "invalid model/delete return code (%d): %s" % (r.status_code, json.dumps(r.json()))

    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"source": "en", "target": "de", "model": filename}, auth=auth)
    assert r.status_code == 200 and not r.json()

    files = {'tgz': (filename, open(file, mode='rb'), 'application/octet-stream')}
    r = requests.post(os.path.join(variables["url"], "model", "add", filename),
                      auth=auth, params=params, files=files)
    assert r.status_code == 200

    r = requests.get(os.path.join(variables["url"], "model/list"),
                     params={"source": "en", "target": "de", "model": filename}, auth=auth)
    assert r.status_code == 200 and r.json()


def test_model_format():
    assert PN9Model.get_model_name(
        "Google_xxyy_GoogleTranslate_June2018") == "GoogleTranslate_June2018"

    assert PN9Model.get_source("Google_xxyy_GoogleTranslate_June2018") == "xx"

    assert PN9Model.get_target("Google_xxyy_GoogleTranslate_June2018") == "yy"

    assert PN9Model.get_author_entity("Google_xxyy_GoogleTranslate_June2018") == "Go"

    assert PN9Model.get_model_user("Google_xxyy_GoogleTranslate_June2018") == "ogl"

    assert PN9Model.get_model_name(
        "SAGPE_enfr_ChouetteMartre_01_59b541da14b5-c8d41") == "ChouetteMartre_01_59b541da14b5-c8d41"

    assert PN9Model.get_source("SAGPE_enfr_ChouetteMartre_01_59b541da14b5") == "en"

    assert PN9Model.get_target("SAGPE_enfr_ChouetteMartre_01_59b541da14b5") == "fr"

    assert PN9Model.get_author_entity("SAGPE_enfr_ChouetteMartre_01_59b541da14b5") == "SA"

    assert PN9Model.get_model_user("SAGPE_enfr_ChouetteMartre_01_59b541da14b5") == "GPE"

    assert PN9Model.get_original_model(
        "DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release") == \
        "DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3"


def test_model_error_detail_without_lp(helper):
    # Login with an standard user of SA
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')

    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])

    assert "trainer" in roles
    assert "admin" not in roles
    assert "SA" == user["entity_code"]

    helper.get('model/list?detail=True&model=Google_xxyy_GoogleTranslate_June2018', 400)


@pytest.mark.skip
def test_model_list_with_trainer(helper):
    # Login with an standard user of SA
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')

    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])

    assert "trainer" in roles
    assert "admin" not in roles
    assert "SA" == user["entity_code"]
    # models = helper.get(
    #     'model/list?detail=True&model=DJLSJ_enfr_BasilicJoyeux_01_1378c32825a14-4ce6a')

    models = helper.get(
        'model/list?detail=True&model=SAJAS_enfr_BouledogueBlanc_01_c754407e209-5be39')
    assert len(models) == 1
    the_model = models[0]
    assert the_model is not None
    assert the_model["model"] == "SAJAS_enfr_BouledogueBlanc_01_c754407e209-5be39"

    models = helper.get('model/list?detail=False&model=Google_xxyy_GoogleTranslate_June2018')
    lps = []
    for model in models:
        lps.append(model['lp'])

    assert "ko_en" in lps
    assert "en_it" in lps
    assert "en_ko" in lps
    assert "en_fr" in lps
    assert "fr_en" in lps

    models = helper.get('model/list?detail=False&source=en&target=fr')
    assert len(models) >= 1272

    sa_model_num = 0
    ss_model_num = 0
    other_model_num = 0
    google_model_num = 0
    other_models = []
    for model in models:
        assert model['lp'] == "en_fr"
        if model['model'].startswith("SA"):
            sa_model_num += 1
        elif model['model'].startswith("SS"):
            ss_model_num += 1
        elif model['model'].startswith("Google"):
            google_model_num += 1
        else:
            other_model_num += 1
            other_models.append(model["model"])

    assert sa_model_num >= 951
    assert ss_model_num >= 318
    assert google_model_num == 1
    assert other_model_num == 2

    # an user of SA cannot see model of DJ
    models = helper.get('model/list?detail=True&DJLSJ_enfr_BasilicJoyeux_01_1378c32825a14-4ce6a')
    assert models is None


@pytest.mark.run(after='test_pushmodel')
def test_sa_trainer_see_concurrency_model(helper):
    helper.set_user('joshua.johanson@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "sa_trainer" in roles
    assert "SS" == user["entity_code"]

    global SA_models
    models = helper.get('model/list?detail=False&source=en&target=de&model=' + SA_models[0])
    assert len(models) == 1


@pytest.mark.run(after='test_pushmodel')
def test_extern_SA_cannot_see_concurrency_model(helper):
    helper.set_user('yonghoon.ji@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "sa_trainer" not in roles
    assert "DJ" == user["entity_code"]

    global SA_models
    models = helper.get('model/list?detail=False&source=en&target=fr&model=' + SA_models[0])
    assert not models


@pytest.mark.skip
def test_model_list_Google_adminSA(helper):
    # Login with an admin
    helper.set_user('gael.perron@systrangroup.com', '0123456789')

    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "SA" == user["entity_code"]
    assert "admin" in roles
    models = helper.get('model/list?detail=False&model=Google_xxyy_GoogleTranslate_June2018')

    lps = []
    for model in models:
        model["model"] == "Google_xxyy_GoogleTranslate_June2018"
        lps.append(model['lp'])

    assert "ko_en" in lps
    assert "en_it" in lps
    assert "en_ko" in lps
    assert "en_fr" in lps
    assert "fr_en" in lps


@pytest.mark.skip
def test_model_list_with_adminSA(helper):
    # Login with an admin
    helper.set_user('gael.perron@systrangroup.com', '0123456789')

    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "SA" == user["entity_code"]
    assert "admin" in roles

    models = helper.get(
        'model/list?detail=True&model=SAJAS_enfr_BouledogueBlanc_01_c754407e209-5be39')
    assert len(models) == 1
    assert models[0] is not None
    assert models[0]["model"] == "SAJAS_enfr_BouledogueBlanc_01_c754407e209-5be39"

    # an user of SA can see model of DJ
    models = helper.get(
        'model/list?detail=True&model=DJLSJ_enfr_BasilicJoyeux_01_1378c32825a14-4ce6a')
    assert len(models) == 1
    assert models[0]["model"] == "DJLSJ_enfr_BasilicJoyeux_01_1378c32825a14-4ce6a"

    models = helper.get('model/list?detail=False&source=en&target=fr')
    assert len(models) >= 1272

    model_nums = {}
    for model in models:
        assert model['lp'] == "en_fr"
        model_nums[model['model'][:2]] = model_nums.get(model['model'][:2], 0) + 1

    assert model_nums["SA"] >= 951
    assert model_nums["SS"] >= 318
    assert model_nums["Go"] == 1
    assert model_nums["DJ"] >= 93
    assert model_nums["CL"] >= 427


@pytest.mark.skip
def test_describe_with_trainer(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    model = helper.get('model/describe/Google_xxyy_GoogleTranslate_June2018')
    assert model["model"] == "google-translate"
    assert model["target"] == "yy"
    assert model["source"] == "xx"
    assert model["imageTag"] == "nmtwizard/google-translate"

    global SA_models
    config = helper.get('model/describe/' + SA_models[0], expected_code=200)
    # assert config == config_ref
    print(config)


def test_describe_access_error(helper):
    helper.set_user('yonghoon.ji@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "sa_trainer" not in roles
    assert "DJ" == user["entity_code"]

    global SA_models
    helper.get('model/describe/' + SA_models[0], expected_code=403)


@pytest.mark.skip
def test_access_to_vocable_file(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "SA" == user["entity_code"]

    config = helper.get('model/describe/SALSH_enko_InsideWasabi_00_fa15e4300d0e485abc5a_vocab')

    assert config is not None


@pytest.mark.skip
def test_error_access_to_vocable_file_from_extern(helper):
    helper.set_user('yonghoon.ji@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "sa_trainer" not in roles
    assert "DJ" == user["entity_code"]

    helper.get('model/describe/SALSH_enko_InsideWasabi_00_fa15e4300d0e485abc5a_vocab',
               expected_code=403)


@pytest.mark.skip
def test_detail_normal_model(helper):
    helper.set_user('koen.vanwinckel@crosslang.com', '0123456789')
    user = helper.get("user/whoami")
    assert "CL" == user["entity_code"]

    response = helper.get('model/listfiles/CLADM_enfr_InsideSkirret_03_d2f688e-d9c84')
    assert len(response) == 14

    for i in ["CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/dict.vocab40k.fr",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/model.ckpt-21817.data-00000-of-00002",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/checkpoint",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/dict.vocab40k.en",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/backward.probs",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/model.ckpt-21817.data-00001-of-00002",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/model.ckpt-21817.meta",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/model.ckpt-21817.index",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/checksum.md5",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/forward.probs",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/config.json",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/joint-bpe32k.en_fr",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/quote_icu.rules",
              "CLADM_enfr_InsideSkirret_03_d2f688e-d9c84/model_description.pkl"]:
        assert i in response


@pytest.mark.skip
def test_detail_release_model(helper):
    helper.set_user('saengjin.lee@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "DJ" == user["entity_code"]

    response = helper.get('model/listfiles/DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release')
    assert len(response) > 1
    assert response == [
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/joint-vocab34k.en_fr',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/checksum.md5',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/ctranslate2_model/',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/vocab32k.en',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/README.md',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/config.json',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/vocab34k.fr']


@pytest.mark.skip
def test_describe_with_trainer(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    model = helper.get('model/describe/Google_xxyy_GoogleTranslate_June2018')
    assert model["model"] == "google-translate"
    assert model["target"] == "yy"
    assert model["source"] == "xx"
    assert model["imageTag"] == "nmtwizard/google-translate"

    config = helper.get('model/describe/SAJAS_enfr_BrownCoreopsis_15_f6fda0bca971-72ed9')
    config_ref = {"mpreprocess": {"source": {
        "noise": {"drop_char_prob": 0.001, "duplicate_char_prob": 0.001, "swap_char_prob": 0.001,
                  "drop_word_prob": 0.001, "unk_injection": 0.0, "drop_space_prob": 0.001},
        "localization_rules": ["${MODEL_DIR}/loca_en-GBtoUS.rules"], "normalization": {
            "character": {"punctuation": "none", "ligatures": True,
                          "icu_rules": ["${MODEL_DIR}/quote_icu.rules"], "numbers": "none"}}},
        "target": {"normalization": {
            "character": {"punctuation": "none", "ligatures": True,
                          "icu_rules": ["${MODEL_DIR}/quote_icu.rules"],
                          "numbers": "none"}}}},
                  "description": "restart from scratch with NaturalMacaw 50 parameters",
                  "source": "en", "parent_model": "SAJAS_enfr_BrownCoreopsis_14_81fb5cea1030-a3669",
                  "modelType": "checkpoint", "bpreprocess": {
            "filter": {"align_perplexity": {"percent_threshold": {"upper": 0, "lower": 0.01}},
                       "char": {"src_non_letter_ratio": 2, "src_alphabets": ["Latin", "Katakana"],
                                "tgt_non_letter_ratio": 2, "tgt_alphabets": ["Latin", "Katakana"]},
                       "length": {"max_src": 100, "max_tgt": 100},
                       "lid": {"source": {"min_length": 30, "nbest": 3},
                               "model": "${TRAIN_DIR}/xx/lid-1.bin",
                               "target": {"min_length": 30, "nbest": 3}},
                       "length_ratio": {"min_ratio_len_src_tgt": 0.4,
                                        "max_ratio_len_src_tgt": 2.5}}, "num_threads": 4,
            "batch_size": 100000,
            "annotate": {"unk": {"initProb": 0.001, "probNext": 0.5}, "basicent": {"probKeep": 0.9},
                         "tag": {"probNextLeft": 0.3, "probRight": 0.05, "probNextRight": 0.3,
                                 "probLeft": 0.05}, "ts": {"initProb": 0.05, "probNext": 0.3},
                         "ud": {"src": "${TRAIN_DIR}/en_fr/ud/ud-enfr-5k-en.dct", "initProb": 0.2,
                                "tgt": "${TRAIN_DIR}/en_fr/ud/ud-enfr-5k-fr.dct"}},
            "alignment_model": {
                "forward": {"probs": "${TRAIN_DIR}/en_fr/word_align/enfr/forward.probs"},
                "backward": {"probs": "${TRAIN_DIR}/en_fr/word_align/enfr/backward.probs"}},
            "icu_translit": [{"prob": 0.02, "rule": "Lower"}, {"prob": 0.03, "rule": "Upper"},
                             {"prob": 0.02, "rule": "Title"},
                             {"prob": 0.01, "rule": "Final-Punctuation-Remove"}], "placeholder": [
                {"ph_threshold": 7.0, "ph_prefix": "ph_unk", "ph_action": "shift",
                 "ph_action_proba": 0.3},
                {"ph_prefix": "ph_ud", "ph_action": "shift", "ph_action_proba": 0.2},
                {"ph_threshold": 10.0, "ph_prefix": "it_tag", "ph_action": "shift",
                 "ph_action_proba": 0.3},
                {"ph_prefix": "ph_ent_uri", "ph_action": "shift", "ph_action_proba": 0.2}]},
        "imageTag": "docker.io/systran/pn9_tf:v1.9.0",
        "build": {"startDate": 1544936489.848547, "cumSentenceCount": 71670358,
                  "endDate": 1544939380.550395, "containerId": "f24785fcdb45",
                  "sentenceCount": 4777851, "distribution": {
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_8": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23407, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_9": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 2789098,
                        "linefiltered": 21588, "linesampled": 21449},
                    "btxt_2dir_en-XX-fr-YY_News__26532-news-commentary-v12": {
                        "pattern": "1-news-commentary", "linecount": 244552,
                        "linefiltered": 234935, "linesampled": 244552},
                    "btxt_2dir_en-CA-fr-CA_Legal__26996-TAUS-PolicyProcess-CanadianGovernment-Download-7701-7720": {
                        "pattern": "1-Legal", "linecount": 893109, "linefiltered": 35170,
                        "linesampled": 36118},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_2": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23363, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_3": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23412, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_0": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23229, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_1": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23425, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_6": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23352, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_7": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23380, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_4": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23260, "linesampled": 23070},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26956-OPUS-OpenSubtitles2018_90p_5": {
                        "pattern": "0-OpenSubtitles2018_90p", "linecount": 3000000,
                        "linefiltered": 23270, "linesampled": 23070},
                    "btxt_2dir_en-GB-fr-CA_IT__26964-TAUS-HW-SalesMarket-Download-7609": {
                        "pattern": "1-IT", "linecount": 638, "linefiltered": 27,
                        "linesampled": 30},
                    "btxt_2dir_en-US-fr-YY_IT__26970-TAUS-HW-Support-Download-7681": {
                        "pattern": "1-IT", "linecount": 365247, "linefiltered": 17076,
                        "linesampled": 17629},
                    "term_enfr_en-XX-fr-YY_Generic__Lookup-finaldict": {
                        "pattern": "1-term_enfr.*Generic__Lookup", "linecount": 208704,
                        "linefiltered": 42868, "linesampled": 45817},
                    "btxt_2dir_en-US-fr-YY_IT__26999-TAUS-Telecom-Support-Download-7681": {
                        "pattern": "1-IT", "linecount": 70775, "linefiltered": 3378,
                        "linesampled": 3416},
                    "btxt_2dir_en-US-fr-YY_IT__26988-TAUS-SW-Support-Download-7681": {
                        "pattern": "1-IT", "linecount": 25336, "linefiltered": 1154,
                        "linesampled": 1222},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25865-visitlondon": {
                        "pattern": "1-Tourism", "linecount": 443, "linefiltered": 242,
                        "linesampled": 238},
                    "btxt_2dir_en-XX-fr-CA_IT__26954-msdn-ui-strings-r2": {
                        "pattern": "1-IT",
                        "linecount": 146496,
                        "linefiltered": 6914,
                        "linesampled": 7070},
                    "btxt_2dir_en-XX-fr-YY_Legal__238-undoc.2000_0": {
                        "pattern": "1-Legal",
                        "linecount": 3000000,
                        "linefiltered": 114868,
                        "linesampled": 121324},
                    "btxt_2dir_en-CA-fr-CA_Legal_Tax_26458-Canada-tax-code": {
                        "pattern": "1-Legal", "linecount": 33165, "linefiltered": 1104,
                        "linesampled": 1341},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26397-tatoeba-r2": {
                        "pattern": "0-tatoeba",
                        "linecount": 212598,
                        "linefiltered": 214343,
                        "linesampled": 212598},
                    "btxt_2dir_en-XX-fr-YY_Legal__109-LDC-UN1": {
                        "pattern": "1-Legal",
                        "linecount": 182160,
                        "linefiltered": 7004,
                        "linesampled": 7366},
                    "btxt_2dir_en-CA-fr-CA_Legal__26995-TAUS-LegalServ-Law-Download-7701_0": {
                        "pattern": "1-Legal", "linecount": 3000000, "linefiltered": 118597,
                        "linesampled": 121324},
                    "btxt_2dir_en-CA-fr-CA_Legal__26995-TAUS-LegalServ-Law-Download-7701_1": {
                        "pattern": "1-Legal", "linecount": 1005812, "linefiltered": 40315,
                        "linesampled": 40676},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25827-appartcity": {
                        "pattern": "1-Tourism", "linecount": 1539, "linefiltered": 830,
                        "linesampled": 830},
                    "btxt_2dir_en-CA-fr-CA_News_Defense_694-journal.forces.ca": {
                        "pattern": "1-News_Defense_694", "linecount": 64585,
                        "linefiltered": 59617, "linesampled": 64585},
                    "term_2dir_en-XX-fr-YY_Dialog__Ready2Go-phrasebook": {
                        "pattern": "1-phrasebook", "linecount": 2792, "linefiltered": 2797,
                        "linesampled": 2792},
                    "btxt_2dir_en-XX-fr-YY_Legal__417-OPUS-EUconst-clean": {
                        "pattern": "1-Legal", "linecount": 4897, "linefiltered": 205,
                        "linesampled": 198},
                    "btxt_2dir_en-US-fr-YY_IT__26983-TAUS-ProfBus-eBayInc-Download-7681": {
                        "pattern": "1-IT", "linecount": 48948, "linefiltered": 2317,
                        "linesampled": 2362},
                    "btxt_2dir_en-GB-fr-YY_Legal__26019-DGT-Acquis": {
                        "pattern": "0-Legal",
                        "linecount": 1869783,
                        "linefiltered": 73774,
                        "linesampled": 89770},
                    "btxt_2dir_en-XX-fr-YY_Legal__424-OPUS-RF-clean": {
                        "pattern": "1-Legal",
                        "linecount": 150,
                        "linefiltered": 6,
                        "linesampled": 6},
                    "btxt_2dir_en-US-fr-YY_IT__26978-TAUS-SW-Instructions-Download-7681": {
                        "pattern": "1-IT", "linecount": 85451, "linefiltered": 3664,
                        "linesampled": 4124},
                    "btxt_2dir_en-GB-fr-YY_Legal__26016-europarl-v7-clean-r5": {
                        "pattern": "1-Legal", "linecount": 1584768, "linefiltered": 64034,
                        "linesampled": 64090},
                    "btxt_2dir_en-GB-fr-YY_Legal__27002-TAUS-LegalServ-HughLawsonTancred-Download-7721": {
                        "pattern": "1-Legal", "linecount": 1378, "linefiltered": 54,
                        "linesampled": 55},
                    "btxt_2dir_en-GB-fr-YY_Misc_Education_26015-EAC-FORMS": {
                        "pattern": "0-Misc", "linecount": 1855, "linefiltered": 1811,
                        "linesampled": 1855},
                    "btxt_2dir_en-US-fr-YY_Legal__26994-TAUS-LegalServ-Law-Download-7681": {
                        "pattern": "1-Legal", "linecount": 56244, "linefiltered": 1901,
                        "linesampled": 2274},
                    "btxt_2dir_en-US-fr-CA_IT__26982-TAUS-ProfBus-eBayInc-Download-7680": {
                        "pattern": "1-IT", "linecount": 26806, "linefiltered": 1279,
                        "linesampled": 1293},
                    "btxt_2dir_en-GB-fr-YY_Legal__27003-TAUS-LegalServ-Law-Download-7721": {
                        "pattern": "1-Legal", "linecount": 298, "linefiltered": 15,
                        "linesampled": 12},
                    "btxt_2dir_en-XX-fr-YY_Tourism__410-easyvoyages-misc": {
                        "pattern": "1-Tourism", "linecount": 9456, "linefiltered": 5051,
                        "linesampled": 5100},
                    "term_2dir_en-US-fr-CA_IT__28134-microsoft-localization": {
                        "pattern": "1-IT", "linecount": 7223, "linefiltered": 344,
                        "linesampled": 348},
                    "btxt_2dir_en-US-fr-CA_IT__26984-TAUS-SW-eBayInc-Download-7680": {
                        "pattern": "1-IT", "linecount": 21682, "linefiltered": 1018,
                        "linesampled": 1046},
                    "term_2dir_en-XX-fr-YY_Generic__26409-enwiki-freebase-all-titles": {
                        "pattern": "1-Generic__26409", "linecount": 685497,
                        "linefiltered": 38890, "linesampled": 45817},
                    "btxt_2dir_en-CA-fr-CA_Legal__110-HANSARD-setA": {
                        "pattern": "1-Legal",
                        "linecount": 2548361,
                        "linefiltered": 101874,
                        "linesampled": 103059},
                    "btxt_2dir_en-US-fr-CA_IT__26965-TAUS-HW-SalesMarket-Download-7680": {
                        "pattern": "1-IT", "linecount": 199344, "linefiltered": 9332,
                        "linesampled": 9621},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25953-bookings-08032013-clean": {
                        "pattern": "1-Tourism", "linecount": 233128, "linefiltered": 126056,
                        "linesampled": 125735},
                    "btxt_2dir_en-GB-fr-YY_Legal__26018-DGT-TM_1": {
                        "pattern": "0-Legal",
                        "linecount": 70341,
                        "linefiltered": 3203,
                        "linesampled": 3377},
                    "btxt_2dir_en-GB-fr-YY_Legal__26018-DGT-TM_0": {
                        "pattern": "0-Legal",
                        "linecount": 3000000,
                        "linefiltered": 132649,
                        "linesampled": 144033},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_0": {
                        "pattern": "1-giga.release2_90p", "linecount": 3000000,
                        "linefiltered": 73171, "linesampled": 75384},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_1": {
                        "pattern": "1-giga.release2_90p", "linecount": 3000000,
                        "linefiltered": 71449, "linesampled": 75384},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_2": {
                        "pattern": "1-giga.release2_90p", "linecount": 3000000,
                        "linefiltered": 70406, "linesampled": 75384},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_3": {
                        "pattern": "1-giga.release2_90p", "linecount": 3000000,
                        "linefiltered": 69959, "linesampled": 75384},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_4": {
                        "pattern": "1-giga.release2_90p", "linecount": 3000000,
                        "linefiltered": 70270, "linesampled": 75384},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_5": {
                        "pattern": "1-giga.release2_90p", "linecount": 3000000,
                        "linefiltered": 71358, "linesampled": 75384},
                    "btxt_2dir_en-XX-fr-YY_Misc__240-giga.release2_90p_6": {
                        "pattern": "1-giga.release2_90p", "linecount": 233397,
                        "linefiltered": 5684, "linesampled": 5864},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25866-visitluxembourg": {
                        "pattern": "1-Tourism", "linecount": 1374, "linefiltered": 717,
                        "linesampled": 741},
                    "btxt_2dir_en-XX-fr-YY_News__27060-Casmacat-GlobalVoices-2017Q3": {
                        "pattern": "0-News", "linecount": 341305, "linefiltered": 334540,
                        "linesampled": 341305},
                    "btxt_2dir_en-XX-fr-YY_Legal__27061-UNv1.0-6way_3": {
                        "pattern": "0-Legal",
                        "linecount": 505634,
                        "linefiltered": 22254,
                        "linesampled": 24275},
                    "btxt_2dir_en-XX-fr-YY_Legal__27061-UNv1.0-6way_2": {
                        "pattern": "0-Legal",
                        "linecount": 3000000,
                        "linefiltered": 133195,
                        "linesampled": 144033},
                    "btxt_2dir_en-XX-fr-YY_Legal__27061-UNv1.0-6way_1": {
                        "pattern": "0-Legal",
                        "linecount": 3000000,
                        "linefiltered": 134237,
                        "linesampled": 144033},
                    "btxt_2dir_en-XX-fr-YY_Legal__27061-UNv1.0-6way_0": {
                        "pattern": "0-Legal",
                        "linecount": 3000000,
                        "linefiltered": 134655,
                        "linesampled": 144033},
                    "btxt_2dir_en-CA-fr-CA_Legal__111-hansard.isi": {
                        "pattern": "0-Legal",
                        "linecount": 912284,
                        "linefiltered": 43597,
                        "linesampled": 43799},
                    "btxt_2dir_en-US-fr-CA_IT__26969-TAUS-HW-Support-Download-7680": {
                        "pattern": "1-IT", "linecount": 24, "linefiltered": 1,
                        "linesampled": 1},
                    "btxt_2dir_en-CA-fr-CA_Legal_Tax_26460-Canada-taxregulations": {
                        "pattern": "1-Legal", "linecount": 9231, "linefiltered": 338,
                        "linesampled": 373},
                    "btxt_2dir_en-XX-fr-YY_IT__141-msdn-vs2005": {
                        "pattern": "1-IT",
                        "linecount": 193783,
                        "linefiltered": 8910,
                        "linesampled": 9353},
                    "btxt_2dir_en-US-fr-YY_IT__26979-TAUS-SW-SalesMarket-Download-7681-7767": {
                        "pattern": "1-IT", "linecount": 87653, "linefiltered": 4015,
                        "linesampled": 4230},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25864-serbia.travel": {
                        "pattern": "1-Tourism", "linecount": 438, "linefiltered": 233,
                        "linesampled": 236},
                    "btxt_2dir_en-XX-fr-YY_IT__422-OPUS-PHP-clean": {
                        "pattern": "1-IT",
                        "linecount": 10470,
                        "linefiltered": 475,
                        "linesampled": 505},
                    "btxt_2dir_en-XX-fr-YY_Tourism__499-timeout-paris-arts-clean": {
                        "pattern": "1-Tourism", "linecount": 57, "linefiltered": 31,
                        "linesampled": 30},
                    "btxt_2dir_en-US-fr-CA_IT__26974-TAUS-SW-StrDoc-Download-7680": {
                        "pattern": "1-IT", "linecount": 130382, "linefiltered": 6166,
                        "linesampled": 6293},
                    "btxt_2dir_en-XX-fr-YY_Tourism__483-ComfortInn-hotels-clean": {
                        "pattern": "1-Tourism", "linecount": 15685, "linefiltered": 8291,
                        "linesampled": 8459},
                    "btxt_2dir_en-GB-fr-YY_IT__26980-TAUS-ProfBus-SalesMarket-Download-7649": {
                        "pattern": "1-IT", "linecount": 38146, "linefiltered": 1744,
                        "linesampled": 1841},
                    "term_2dir_en-US-fr-YY_IT__28135-microsoft-localization": {
                        "pattern": "1-IT", "linecount": 30480, "linefiltered": 1408,
                        "linesampled": 1471},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25828-corpus-parisinfo": {
                        "pattern": "1-Tourism", "linecount": 33699, "linefiltered": 16703,
                        "linesampled": 18175},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25857-easyvoyage-hotels": {
                        "pattern": "1-Tourism", "linecount": 137698, "linefiltered": 73910,
                        "linesampled": 74266},
                    "btxt_2dir_en-US-fr-YY_IT__26968-TAUS-HW-StrDoc-Download-7681": {
                        "pattern": "1-IT", "linecount": 385818, "linefiltered": 17914,
                        "linesampled": 18621},
                    "btxt_2dir_en-XX-fr-YY_Tourism__500-timeout-paris-restaurants-clean": {
                        "pattern": "1-Tourism", "linecount": 670, "linefiltered": 361,
                        "linesampled": 361},
                    "btxt_2dir_en-XX-fr-YY_IT__26955-msdn-ui-strings-r2": {
                        "pattern": "1-IT",
                        "linecount": 2133599,
                        "linefiltered": 99847,
                        "linesampled": 102980},
                    "btxt_2dir_en-XX-fr-YY_Legal_Tax_26459-Bloomberg-taxdocs-TM01-02-05-06-07": {
                        "pattern": "1-Legal", "linecount": 3401, "linefiltered": 127,
                        "linesampled": 137},
                    "btxt_2dir_en-CA-fr-CA_IT__26976-TAUS-SW-StrDoc-Download-7701": {
                        "pattern": "1-IT", "linecount": 2270, "linefiltered": 112,
                        "linesampled": 109},
                    "btxt_2dir_en-GB-fr-YY_Misc__26993-TAUS-LegalServ-Eurostar-HughLawsonTancred-Download-7649": {
                        "pattern": "1-Legal", "linecount": 97, "linefiltered": 0,
                        "linesampled": 3},
                    "btxt_2dir_en-XX-fr-YY_Tourism__496-hotels.com-clean": {
                        "pattern": "1-Tourism", "linecount": 112861, "linefiltered": 60578,
                        "linesampled": 60870},
                    "btxt_2dir_en-US-fr-CA_Instruction__27000-TAUS-TourismArts-Instructions-Download-7680": {
                        "pattern": "1-Tourism", "linecount": 1076, "linefiltered": 538,
                        "linesampled": 580},
                    "btxt_2dir_en-US-fr-YY_IT__26963-TAUS-HW-Intel-Download-7681": {
                        "pattern": "1-IT", "linecount": 41996, "linefiltered": 1939,
                        "linesampled": 2026},
                    "btxt_2dir_en-GB-fr-YY_Legal__26017-DCEP": {
                        "pattern": "1-Legal",
                        "linecount": 2228825,
                        "linefiltered": 82735,
                        "linesampled": 90137},
                    "btxt_2dir_en-XX-fr-CH_News__26899-SwissAdmin-press-releases-20140611": {
                        "pattern": "1-News__26899", "linecount": 47854, "linefiltered": 46034,
                        "linesampled": 47854},
                    "btxt_2dir_en-XX-fr-YY_Misc__443-commoncrawl_90p": {
                        "pattern": "1-commoncrawl_90p", "linecount": 2124047,
                        "linefiltered": 456997, "linesampled": 458174},
                    "btxt_2dir_en-US-fr-YY_IT__26967-TAUS-HW-SalesMarket-Download-7681-7767": {
                        "pattern": "1-IT", "linecount": 978170, "linefiltered": 45574,
                        "linesampled": 47212},
                    "btxt_2dir_en-XX-fr-YY_Tourism__25858-francetourisme": {
                        "pattern": "1-Tourism", "linecount": 1531, "linefiltered": 798,
                        "linesampled": 825},
                    "btxt_2dir_en-US-fr-YY_News__26997-TAUS-ReportsResearch-SebastiaanVandenbore-Download-7681": {
                        "pattern": "1-News__26997", "linecount": 72, "linefiltered": 71,
                        "linesampled": 72},
                    "btxt_2dir_en-XX-fr-YY_Dialog__26398-ted-talks-fbk-r2": {
                        "pattern": "1-ted-talks", "linecount": 231419, "linefiltered": 229929,
                        "linesampled": 231419},
                    "btxt_2dir_en-US-fr-YY_IT__26975-TAUS-SW-StrDoc-Download-7681_0": {
                        "pattern": "1-IT", "linecount": 3000000, "linefiltered": 140902,
                        "linesampled": 144797},
                    "btxt_2dir_en-US-fr-YY_IT__26975-TAUS-SW-StrDoc-Download-7681_1": {
                        "pattern": "1-IT", "linecount": 1168359, "linefiltered": 53507,
                        "linesampled": 56391},
                    "btxt_2dir_en-XX-fr-YY_Legal__238-undoc.2000_2": {
                        "pattern": "1-Legal",
                        "linecount": 2840824,
                        "linefiltered": 108259,
                        "linesampled": 114887},
                    "btxt_2dir_en-US-fr-YY_IT__26981-TAUS-ProfBus-SalesMarket-Download-7681": {
                        "pattern": "1-IT", "linecount": 4820, "linefiltered": 234,
                        "linesampled": 232},
                    "btxt_2dir_en-XX-fr-YY_Legal__238-undoc.2000_1": {
                            "pattern": "1-Legal",
                            "linecount": 3000000,
                            "linefiltered": 114552,
                            "linesampled": 121324},
                    "btxt_2dir_en-GB-fr-YY_Legal__26013-jrc-2011-clean-r3": {
                        "pattern": "0-Legal", "linecount": 1819573, "linefiltered": 84214,
                        "linesampled": 87359},
                    "btxt_2dir_en-XX-fr-YY_Tourism__1401-easyvoyages-tm": {
                        "pattern": "1-Tourism", "linecount": 267675, "linefiltered": 143265,
                        "linesampled": 144368},
                    "btxt_2dir_en-XX-fr-YY_Tourism__408-easyvoyages-hotels-experts": {
                        "pattern": "1-Tourism", "linecount": 27719, "linefiltered": 14843,
                        "linesampled": 14950},
                    "btxt_2dir_en-XX-fr-YY_Tourism__494-entrechefs-clean": {
                        "pattern": "1-Tourism", "linecount": 4457, "linefiltered": 2344,
                        "linesampled": 2403},
                    "btxt_2dir_en-GB-fr-YY_IT__26966-TAUS-HW-SalesMarket-Download-7649-7721": {
                        "pattern": "1-IT", "linecount": 2584, "linefiltered": 111,
                        "linesampled": 124},
                    "btxt_2dir_en-GB-fr-YY_Misc_Education_26014-EAC-REFRENCE-DATA": {
                        "pattern": "0-Misc", "linecount": 1508, "linefiltered": 1489,
                        "linesampled": 1508},
                    "btxt_2dir_en-XX-fr-YY_IT__418-OPUS-OpenOffice-clean": {
                            "pattern": "1-IT",
                            "linecount": 24787,
                            "linefiltered": 1189,
                            "linesampled": 1196},
                    "btxt_2dir_en-GB-fr-YY_IT__26977-TAUS-SW-Instructions-Download-7649": {
                        "pattern": "1-IT", "linecount": 43704, "linefiltered": 2004,
                        "linesampled": 2109},
                    "btxt_2dir_en-US-fr-YY_IT__26985-TAUS-SW-eBayInc-Download-7681": {
                        "pattern": "1-IT", "linecount": 51847, "linefiltered": 2440,
                        "linesampled": 2502},
                    "btxt_2dir_en-XX-fr-YY_IT__26945-OPUS-KDE4": {
                        "pattern": "1-IT",
                        "linecount": 165868,
                        "linefiltered": 6825,
                        "linesampled": 8005}}},
        "target": "fr", "model": "SAJAS_enfr_BrownCoreopsis_15_f6fda0bca971-72ed9",
        "tokenization": {"source": {"bpe_model": "${MODEL_DIR}/joint-bpe32k.en_fr",
                                    "vocabulary": "${MODEL_DIR}/vocab32k.en",
                                    "preserve_placeholders": True, "mode": "aggressive",
                                    "preserve_segmented_tokens": True,
                                    "segment_numbers": True, "segment_case": True,
                                    "joiner_annotate": True},
                         "target": {"bpe_model": "${MODEL_DIR}/joint-bpe32k.en_fr",
                                    "vocabulary": "${MODEL_DIR}/vocab34k.fr",
                                    "preserve_placeholders": True, "mode": "aggressive",
                                    "preserve_segmented_tokens": True,
                                    "segment_numbers": True, "segment_case": True,
                                    "joiner_annotate": True}},
        "data": {"sample": 5000000, "sample_unique": True, "train_dir": "en_fr",
                 "sample_dist": [{"path": "train",
                                  "distribution": [["tatoeba", "*"], ["Legal", 0.18],
                                                   ["Misc", "*"],
                                                   ["OpenSubtitles2018_90p", 0.05],
                                                   ["News", "*"]]},
                                 {"path": "train_restricted",
                                  "distribution": [["Tourism", 0.1],
                                                   ["commoncrawl_90p", 0.1],
                                                   ["giga.release2_90p", 0.1],
                                                   ["ted-talks", "*"],
                                                   ["IT", 0.1, {"bpreprocess": {"filter": {"char": {
                                                                  "src_alphabets": ["Latin", "Greek"],
                                                                  "tgt_alphabets": ["Latin", "Greek"]}}}}],
                                                   ["news-commentary", "*"],
                                                   ["News_Defense_694", "*"],
                                                   ["News__26997", "*"],
                                                   ["News__26899", "*"],
                                                   ["term_enfr.*Generic__Lookup", 0.02],
                                                   ["phrasebook", "*"],
                                                   ["Generic__26409", 0.01, {
                                                       "bpreprocess": {"filter": {"lid": {
                                                           "source": {"min_length": 17,
                                                                      "nbest": 3},
                                                           "model": "${TRAIN_DIR}/xx/lid-1.bin",
                                                           "target": {"min_length": 17,
                                                                      "nbest": 3}}}}}],
                                                   ["Legal", 0.18]]}]},
        "options": {"model_type": "Transformer", "auto_config": True,
                    "config": {"train": {"average_last_checkpoints": 0}}},
        "name": "Transformer 4GPUs"}
    assert config == config_ref


@pytest.mark.skip
def test_describe_release_model(helper):
    helper.set_user('saengjin.lee@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "DJ" == user["entity_code"]

    response = helper.get('model/listfiles/DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release')
    assert len(response) > 1
    assert response == [
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/joint-vocab34k.en_fr',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/checksum.md5',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/ctranslate2_model/',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/vocab32k.en',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/README.md',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/config.json',
        u'DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/vocab34k.fr']


@pytest.mark.skip
def test_detail_vocable_model(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "SA" == user["entity_code"]

    response = helper.get('model/listfiles/SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab')

    assert response == [
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/loca_en-GBtoUS.rules',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/README.md',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/checksum.md5',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/KO_pre-token.rules',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/bpe_en-40k.en',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/en.dct',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/vocab_ko-44k.ko',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/bpe_ko-32k.ko',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/config.json',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/quote_icu.rules',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/vocab_en-41k.en',
        u'SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/ko.dct']


@pytest.mark.skip
def test_detail_error_permission_to_vocab(helper):
    helper.set_user('koen.vanwinckel@crosslang.com', '0123456789')
    user = helper.get("user/whoami")
    assert "CL" == user["entity_code"]
    helper.get('model/listfiles/SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab',
               expected_code=403)


@pytest.mark.skip
def test_get_file_of_release_model(helper):
    helper.set_user('saengjin.lee@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "DJ" == user["entity_code"]

    response = helper.get(
        'model/getfile/DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/joint-vocab34k.en_fr')
    assert len(response.data) == 282044

    response = helper.get(
        'model/getfile/DJLSJ_enfr_AddaxFier_01_627867fa204948658-4f8d3_release/joint-vocab34k.en_fr',
        params={'is_compressed': True})
    assert len(gzip.GzipFile('', 'r', 0, StringIO(response.data)).read()) == 282044


@pytest.mark.skip
def test_get_file_of_normal_model(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "SA" == user["entity_code"]

    response = helper.get(
        'model/getfile/SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/vocab_ko-44k.ko')
    assert len(response.data) == 905010

    response = helper.get(
        'model/getfile/SALSH_enko_RichBuzzard_00_b33c8eb5cca74ddf88970_vocab/vocab_ko-44k.ko',
        params={'is_compressed': True})

    assert len(gzip.GzipFile('', 'r', 0, StringIO(response.data)).read()) == 905010


@pytest.mark.skip
def test_owner_model(helper):
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "SA" == user["entity_code"]

    models = helper.get(
        'model/list?detail=True&model=SALMA_enfr_IguaneAnxieux_01_be46aaa013224-f0a5b')

    assert len(models) == 1
    the_model = models[0]
    assert the_model['model'] == 'SALMA_enfr_IguaneAnxieux_01_be46aaa013224-f0a5b'
    assert the_model['owner']['entity_code'] == 'SA'


@pytest.mark.run(after='test_pushmodel')
def test_author_delete_its_model(helper):
    global SA_models
    helper.set_user('leidiana.martins@systrangroup.com', '0123456789')
    r = helper.get("model/delete/en/de/" + SA_models[0], {"recursive": 1, "dryrun": 1})
    assert SA_models[0] in r


@pytest.mark.run(after='test_pushmodel')
def test_change_model_owner(helper):
    helper.set_user('josep.crego@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    roles = map(lambda e: e['name'], user['roles'])
    assert "SA" == user["entity_code"]
    assert "ss_trainer" in roles

    global SA_models
    model_name = SA_models[1]
    models = helper.get('model/list?detail=True&model=%s' % model_name)

    assert len(models) == 1
    the_model = models[0]
    assert the_model['model'] == model_name
    assert the_model['owner']['entity_code'] == 'SA'

    modified_model = helper.post("model/%s/owner/%s" % (model_name, "SS"), None)
    assert modified_model["owner"]["entity_code"] == "SS"


@pytest.mark.run(after='test_change_model_owner')
def test_SS_can_delete_its_model_created_by_SA(helper):
    helper.set_user('joshua.johanson@systrangroup.com', '0123456789')
    user = helper.get("user/whoami")
    assert "SS" == user["entity_code"]

    global SA_models
    model = SA_models[1]  # this model is changed to SS owner from previous test
    # model = 'SALMA_ende_StarkeZucchini_01_f5dc428dbe984182b7'
    models = helper.get('model/list?detail=False&model=%s' % model)

    assert models and len(models) == 1 and models[0]

    the_model = models[0]
    assert the_model['owner']['entity_code'] == 'SS'

    models_to_delete = helper.get("model/delete/en/de/%s" % model, {"recursive": 1, "dryrun": 1})
    assert model in models_to_delete
