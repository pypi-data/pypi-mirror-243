import os
import pytest
from io import BytesIO


@pytest.mark.usefixtures("mock_cm2")
def test_list_dataset(variables, client):
    auth = (variables['admin_user'], variables['admin_password'])
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    assert isinstance(r.json, list) and len(r.json) > 0, "there should be at least 1 dataset"
    # check dataset description is ok
    dataset = r.json[0]
    assert isinstance(dataset, dict)
    assert "creator" in dataset
    assert "entity" in dataset
    assert "name" in dataset
    assert "service" in dataset
    assert "source_language" in dataset
    assert "target_language" in dataset
    assert "lp" in dataset
    assert "created_at" in dataset

    # get dataset files list
    dataset_id = str(dataset['_id']['$oid'])
    r = client.get(f"/dataset/{dataset_id}/files/list", auth=auth)
    assert isinstance(r.json, list) and len(r.json) > 0, "there should be at least 1 corpus in dataset"
    res = r.json
    corpus_detail = res[0]
    assert "alias_names" in corpus_detail
    assert "entries" in corpus_detail
    assert "errorDesc" in corpus_detail
    assert "id" in corpus_detail
    assert "key" in corpus_detail
    assert "format" in corpus_detail
    assert "sourceLanguage" in corpus_detail and corpus_detail["sourceLanguage"] == dataset["source_language"]
    assert "targetLanguages" in corpus_detail
    assert "type" in corpus_detail and corpus_detail["type"] in ["train", "test"]

    # get list segments from corpus
    corpus_id = corpus_detail['id']
    params = {"limit": 1}
    r = client.get(f"/dataset/{dataset_id}/files/{corpus_id}/segments/list", query_string=params, auth=auth)
    assert isinstance(r.json, dict)
    res = r.json
    assert "dataset" in res
    assert "lp" in res
    assert "key" in res
    assert "data" in res
    assert "skip" in res
    assert "limit" in res
    assert "filter" in res
    assert "total" in res


@pytest.mark.usefixtures("mock_cm2")
def test_add_dataset(variables, client):
    auth = (variables['admin_user'], variables['admin_password'])
    data = {
        "dataset_name": "new_dataset",
        "source_language": "en",
        "target_language": "fr",
        "testing_proportion": '{"isPercentage": true, "value": 10}'
    }
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/corpus/en_fr/testing_upload.txt', 'rb') as corpus_file:
        file_data = corpus_file.read()
    file_stream = BytesIO(file_data)
    file_stream.seek(0)
    data['model_data'] = (file_stream, 'testing_upload.txt')
    r = client.post("/dataset/add", data=data, auth=auth)
    assert r.status_code == 200
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    latest_dataset = r.json[-1]
    assert latest_dataset['name'] == 'new_dataset'


@pytest.mark.usefixtures("mock_cm2")
def test_cannot_add_invalid_dataset(variables, client):
    auth = (variables['admin_user'], variables['admin_password'])
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    num_of_datasets_before = len(r.json)

    # Check duplicate dataset name
    data = {
        "dataset_name": "dataset_for_test",
        "source_language": "en",
        "target_language": "fr",
        "testing_proportion": '{"isPercentage": true, "value": 10}'
    }
    r = client.post("/dataset/add", data=data, auth=auth)
    assert r.status_code == 400

    # Check invalid dataset name
    data["dataset_name"] = "dataset @@!"
    r = client.post("/dataset/add", data=data, auth=auth)
    assert r.status_code == 400

    # Check invalid upload corpus name
    data["dataset_name"] = "invalid_corpus_name"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/corpus/en_fr/testing_upload.txt', 'rb') as corpus_file:
        file_data = corpus_file.read()
    file_stream = BytesIO(file_data)
    file_stream.seek(0)
    data['model_data'] = (file_stream, 'upload_corpus_@@!.txt')
    r = client.post("/dataset/add", data=data, auth=auth)
    assert r.status_code == 400

    # Check number of datasets in db not change
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    assert len(r.json) == num_of_datasets_before


@pytest.mark.usefixtures("mock_cm2")
def test_add_corpus_to_dataset(variables, client):
    auth = (variables['admin_user'], variables['admin_password'])
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    latest_dataset = r.json[-1]
    dataset_id = str(latest_dataset['_id']['$oid'])

    data = {
        "source_language": "en",
        "target_language": "fr",
    }
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/corpus/en_fr/training_upload.txt', 'rb') as corpus_file:
        file_data = corpus_file.read()
    file_stream = BytesIO(file_data)
    file_stream.seek(0)
    data['training_data'] = (file_stream, 'training_upload.txt')
    r = client.post(f"/dataset/{dataset_id}/files/add", data=data, auth=auth)
    assert r.status_code == 200


@pytest.mark.usefixtures("mock_cm2")
def test_handling_segments_in_corpus(variables, client):
    auth = (variables['admin_user'], variables['admin_password'])
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    latest_dataset = r.json[-1]
    dataset_id = str(latest_dataset['_id']['$oid'])
    corpus_id = '645728841c44e5ed2509ea88'

    # add segments to corpus
    data = {'segments': [{'language': 'en', 'seg': 'Bonjour', 'tgts': [{'language': 'fr', 'seg': 'Hello'}]}]}
    r = client.post(f"/dataset/{dataset_id}/files/{corpus_id}/add", json=data, auth=auth)
    assert r.status_code == 200

    # modify segment from corpus
    data = {'target_value': 'Hi', 'target_id': '645770b81c44e5ed2509f20c', 'source_value': 'Bonjour'}
    seg_id = f'{corpus_id}.645770b81c44e5ed2509f20b'
    r = client.post(f"/dataset/{dataset_id}/files/{corpus_id}/segments/{seg_id}/modify", json=data, auth=auth)
    assert r.status_code == 200

    # delete segment from corpus
    data = {'segments': [seg_id]}
    r = client.post(f"/dataset/{dataset_id}/files/{corpus_id}/delete", json=data, auth=auth)
    assert r.status_code == 200


@pytest.mark.usefixtures("mock_cm2")
def test_delete_files_from_dataset(variables, client, requests_mock):
    json = {'directories': [], 'files': [
        {'accountId': '5f31564ec8466a0009253392', 'checksum': '0070473a-69e4-4826-86c5-4b31137e0d66',
         'completedAt': 'Sun May  7 04:26:44 2023\n', 'createdAt': 'Sun May  7 04:26:44 2023\n',
         'features': {'es1': {'status': 'ok'}, 'fuzzy': {'status': 'ok'}},
         'filename': '/SA/new_dataset/train/training_upload.txt', 'format': 'text/bitext',
         'id': '645728841c44e5ed2509ea88',
         'importOptions': '{"cleanFormatting":true,"expectedSourceLanguage":"en",'
                          '"expectedTargetLanguages":["fr"],"removeDuplicates":true}',
         'nbSegments': '62', 'sourceLanguage': 'en', 'sourceLanguageCode': 'en', 'status': 'ok',
         'targetLanguageCodes': ['fr'], 'targetLanguages': ['fr']}]}
    requests_mock.get(f'{variables["cm2_url"]}/corpus/list', json=json)

    auth = (variables['admin_user'], variables['admin_password'])
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    latest_dataset = r.json[-1]
    dataset_id = str(latest_dataset['_id']['$oid'])
    data = {"path": "SA/new_dataset/train/training_upload.txt"}
    r = client.delete(f"/dataset/{dataset_id}/files/delete", data=data,
                      content_type='application/x-www-form-urlencoded', auth=auth)
    assert r.status_code == 200


@pytest.mark.usefixtures("mock_cm2")
def test_delete_dataset(variables, client):
    auth = (variables['admin_user'], variables['admin_password'])
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    latest_dataset = r.json[-1]
    dataset_id = str(latest_dataset['_id']['$oid'])
    r = client.delete(f"/dataset/{dataset_id}/delete", auth=auth)
    assert r.status_code == 200
    r = client.get("/dataset/list", auth=auth)
    assert r.status_code == 200
    assert 'new_dataset' not in [item['name'] for item in r.json]
