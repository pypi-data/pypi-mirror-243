import pytest


# TEST: test_lu
# Goal: get user SAADM
@pytest.mark.usefixtures("teardown_db")
def test_lu(helper):
    users = helper.get_users()
    assert len(users) >= 1

    # check different field are correct
    systran_admin_user = next(item for item in users if item['tid'] == 'SAADM')
    assert systran_admin_user
    assert systran_admin_user['email'] == 'admin@systran.fr'
    assert systran_admin_user['entity_code'] == 'SA'
    assert systran_admin_user['name'] == 'Admin Systran'
    assert systran_admin_user['entity'] == 'SYSTRAN SA'


@pytest.mark.usefixtures("teardown_db")
def test_error_duplicate_user(helper):
    num_of_users_before = helper.count_user()
    # cannot user with incorrect user_code
    helper.post("user/add",
                {'first_name': 'john.doe', 'last_name': 'doe', 'email': 'doe.john@systran.fr',
                 'password': 'Systran@123456', 'user_code': 'XX'}, 400)

    assert helper.count_user() == num_of_users_before
    # Cannot user twice with a user_code already existing
    user_created_id = helper.post("user/add", {'first_name': 'coco', 'last_name': 'belmondo',
                                               'email': 'coco.belmondo@systran.fr',
                                               'password': 'Systran@123456',
                                               'user_code': 'LOL'}, 424)

    assert helper.count_user() == num_of_users_before
    assert user_created_id != 0

    # password format error
    user_created_id = helper.post("user/add",
                                  {'entity_id': 3, 'first_name': 'john', 'last_name': 'doe',
                                   'email': 'xxx@airbus.fr', 'password': '000', 'user_code': 'JDE',
                                   'roles': []}, 400)

    assert helper.count_user() == num_of_users_before
    assert user_created_id != 0


@pytest.mark.usefixtures("teardown_db")
def test_error_creating_user(helper):
    # admin user cannot add user with other company
    airbus_entity_id = 3
    admin_user_permission_id = 2
    role_airbus_admin = helper.add_role({'name': 'airbus_admin', 'entity_id': airbus_entity_id,
                                         'permissions': [{'permission': admin_user_permission_id}]})
    user_created_id = helper.post("user/add", {'first_name': 'coco', 'last_name': 'belmondo',
                                               'email': 'coco.belmondo@airbus.fr',
                                               'password': 'Systran@123456',
                                               'user_code': 'COC', 'entity_id': airbus_entity_id})

    assert user_created_id != 0

    helper.modify_users({'user_id': user_created_id, 'roles': [role_airbus_admin['id']]})

    helper.set_user('coco.belmondo@airbus.fr', 'Systran@123456')

    thales_entity_id = 2

    # ok within the same entity Airbus
    helper.post("user/add",
                {'first_name': 'tibo', 'last_name': 'colococ', 'entity_id': airbus_entity_id,
                 'email': 'xxx@airbus.fr', 'password': 'Systran@123456', 'user_code': 'JDE'})

    # error when creating a user in Thales entity
    helper.post("user/add",
                {'first_name': 'tibo', 'last_name': 'colococ', 'entity_id': thales_entity_id,
                 'email': 'xxx@airbus.fr', 'password': 'Systran@123456', 'user_code': 'JDE'}, 403)


@pytest.mark.usefixtures("teardown_db")
def test_error_modify_user(helper):
    # create a role in the thales entity
    thales_entity_id = 4
    systran_user_id = 2
    role_thales_trainer = helper.add_role({'name': 'thales_trainer', 'entity_id': thales_entity_id,
                                           'permissions': [{'permission': 6}]})

    # Error when giving a role onwed by Thales entity to a Systran user
    new_systran_user = {'user_id': systran_user_id, 'roles': role_thales_trainer['id']}

    helper.post('user/modify', new_systran_user, expected_code=424)


@pytest.mark.usefixtures("teardown_db")
def test_exttoken(helper):
    helper.login(helper.user, helper.password, None)

    helper.login('LOLO.FERNANdel@systran.fr', '0123456789', None)

    helper.login('lolo.fernandel@systraN.fr', '0123456789', 1000)

    helper.login('lolo.fernandel@systran.f', '0123456789', 1000, expected_code=401)


@pytest.mark.usefixtures("teardown_db")
def test_delete_user(helper):
    # prepare some testing data
    systran_entity_id = 1
    user_data = {'first_name': 'cocoxxx', 'last_name': 'belmondox', 'email': 'cocoxxx.belmondox@systran.fr',
                 'password': 'Systran@123456', 'user_code': 'COE', 'entity_id': systran_entity_id}
    user_id = helper.add_user(user_data)

    # delete the user with success
    helper.post('user/delete', {'user_id': user_id})

    # a simple user cannot delete another user
    helper.add_user(user_data)

    helper.set_user('lolo.fernandel@systran.fr ', '0123456789')
    helper.post('user/delete', {'user_id': user_id}, expected_code=403)


"""
Test : test_add_modify_entity
Goal: add / modify entity
"""


@pytest.mark.usefixtures("teardown_db")
def test_add_modify_entity(helper):
    # Test: add some entities
    disney_entity = helper.add_entity(
        {'name': 'disney', 'entity_code': 'DS', 'email': 'a@disney.fr'})
    helper.add_entity({'name': 'bnpparibas', 'entity_code': 'BN', 'email': 'a@bnp.fr'})

    # Test: modify an entity
    disney_new = {'entity_id': disney_entity['id'], 'name': 'disneys', 'email': 'a@disney.com',
                  'description': 'blabla', 'tel': '2132', 'address': '23 rue bidon 77200 MLV'}

    disney_entity_modified = helper.modify_entity(disney_new)

    assert disney_entity_modified['id'] == disney_entity['id']
    assert disney_entity_modified['entity_code'] == disney_entity['entity_code']
    assert disney_entity_modified['name'] == disney_new['name']
    assert disney_entity_modified['email'] == disney_new['email']
    assert disney_entity_modified['description'] == disney_new['description']
    assert disney_entity_modified['address'] == disney_new['address']


"""
Test : test_disable_enable_entity
Goal: disable / enable an entity
"""


@pytest.mark.usefixtures("teardown_db")
def test_disable_enable_entity(helper):
    airbus_entity_id = 3
    airbus_data = helper.get_entity(airbus_entity_id)
    assert airbus_data['active'] is True

    helper.post('entity/disable', {'entity_id': airbus_entity_id})
    airbus_data = helper.get_entity(airbus_entity_id)
    assert airbus_data['active'] is False

    helper.post('entity/enable', {'entity_id': airbus_entity_id})
    airbus_data = helper.get_entity(airbus_entity_id)
    assert airbus_data['active'] is True


""" Test: test_get_role
 Goal: get all roles or a role by Id
"""


@pytest.mark.usefixtures("teardown_db")
def test_get_role(helper):
    role_by_list = next(item for item in helper.get_roles()
                        if item['name'] == "airbus_share_push" and item['entity_id'] == 3)

    assert role_by_list['name'] == 'airbus_share_push'

    role_by_id = helper.get('role/' + str(role_by_list['id']) + '?detail=True')
    assert role_by_id
    assert role_by_id['name'] == role_by_list['name']


""" Test: test_shared_role
 Goal:
 - share a permission with other entities
 - remove a permission from a shared role, ref ticket 51888
 - remove a shared entity from the role
 - remove completely the role
"""


@pytest.mark.usefixtures("teardown_db")
def test_shared_role(helper):
    permissions = helper.get_permissions()
    permission_to_share = next(item for item in permissions if item['name'] == 'push_model')

    airbus_data = helper.get_entity(3)
    thales_data = helper.get_entity(4)
    vinci_data = helper.get_entity(5)

    # TEST: get role list
    role_push_airbus_to_share = next(item for item in helper.get_roles()
                                     if
                                     item['name'] == "airbus_share_push" and item['entity_id'] == 3)

    assert role_push_airbus_to_share

    # TEST: Airbus share push_model role with Vinci and Thales entities
    helper.share_role(role_push_airbus_to_share, airbus_data, thales_data)
    helper.share_role(role_push_airbus_to_share, airbus_data, vinci_data)

    shared_role_created = next(item for item in helper.get_roles()
                               if item['name'] == "airbus_share_push" and item['entity_id'] ==
                               airbus_data['id'])

    shared_entities_codes = [e['entity_id'] for e in shared_role_created["shared_entities"]]

    assert vinci_data['id'] in shared_entities_codes
    assert thales_data['id'] in shared_entities_codes

    # TEST: remove the local permission same as the shared permission
    # Vinci creates new role to be able to use the Aribus's shared permission

    permission_to_release = next(item for item in permissions if item['name'] == 'release_model')
    role_vinci_use_airbus_perm = {'name': 'vinci_use_aribus_perm', 'entity_id': vinci_data['id'],
                                  'permissions': [{'permission': permission_to_share['id'],
                                                   'entity': airbus_data['id']},
                                                  {'permission': permission_to_share['id'],
                                                   'entity': vinci_data['id']},
                                                  # same permission but different entity
                                                  {'permission': permission_to_release['id'],
                                                   'entity': vinci_data['id']}
                                                  ]}

    role_vinci_use_airbus_perm_created = helper.add_role(role_vinci_use_airbus_perm)

    role_vinci_use_airbus_perm = {'name': role_vinci_use_airbus_perm_created['name'],
                                  'role_id': role_vinci_use_airbus_perm_created['id'],
                                  'permissions': [{'permission': permission_to_share['id'],
                                                   'entity': airbus_data['id']},
                                                  {'permission': permission_to_release['id'],
                                                   'entity': vinci_data['id']}
                                                  ]}

    helper.modify_role(role_vinci_use_airbus_perm)

    # Test 3: remove Vinci entity from the shared role
    helper.post("role/share/remove",
                {'src_entity_id': airbus_data['id'], 'dest_entity_id': vinci_data['id'],
                 'role_id': shared_role_created['id']})

    shared_role_modified = next(
        item for item in helper.get_roles() if item['id'] == shared_role_created['id'])

    shared_entities_codes = [e['entity_id'] for e in shared_role_modified["shared_entities"]]

    assert vinci_data['id'] not in shared_entities_codes
    assert thales_data['id'] in shared_entities_codes

    # Test 4: remove the role
    helper.post("role/delete", {'role_id': shared_role_created['id']})
    role_ids = [o['id'] for o in helper.get_roles()]
    assert shared_role_created['id'] not in role_ids


"""
 TEST: test_user
 GOAL:
 - create an user with a role
 - give it a role
 - disable/enable/delete the use
"""


@pytest.mark.usefixtures("teardown_db")
def test_error_duplicate_user(helper):
    trainer_role = next(item for item in helper.get_roles() if item['name'] == 'trainer')
    lingadmin_role = next(item for item in helper.get_roles() if item['name'] == 'lingadmin')
    assert trainer_role

    data = {
        'first_name': 'coco3',
        'last_name': 'belmondo',
        'email': 'coco3.belmondo@systran.fr',
        'password': 'Systran@123456',
        'user_code': 'COR'
    }

    # TEST: create the user
    helper.post("user/add", data)

    # check the user is right created: item['tid'][-3] == data['user_code'] and
    user_created = next(item for item in helper.get_users() if item['email'] == data['email'])
    assert user_created

    helper.post("user/add", data, expected_code=424)


"""
 TEST: test_user
 GOAL:
 - create an user with a role
 - give it a role
 - disable/enable/delete the use
"""


@pytest.mark.usefixtures("teardown_db")
def test_user(helper):
    trainer_role = next(item for item in helper.get_roles() if item['name'] == 'trainer')
    lingadmin_role = next(item for item in helper.get_roles() if item['name'] == 'lingadmin')
    assert trainer_role

    data = {
        'first_name': 'coco_3',
        'last_name': 'belmondo',
        'email': 'coco_3.belmondo2@systran.fr',
        'password': 'Systran@123456',
        'user_code': 'COS'
    }

    # TEST: create the user
    helper.post("user/add", data)

    # check the user is right created: item['tid'][-3] == data['user_code'] and
    user_created = next(item for item in helper.get_users() if item['email'] == data['email'])
    assert user_created

    # Test: give role to the user
    data['roles'] = [trainer_role['id'], lingadmin_role['id']]
    data['user_id'] = user_created['id']
    helper.modify_users(data)

    trainer_user_created = next(
        item for item in helper.get_users() if item['id'] == data['user_id'])

    # TEST: associate the user to a group:
    entity_id = 1
    helper.post('group/add', {'name': 'mytestgroup', 'entity_id': entity_id, 'roles': [3, 4]})

    group_created = next(item for item in helper.get('group/list?detail=True')
                         if item['name'] == 'mytestgroup' and item['entity_id'] == entity_id)

    data['groups'] = [group_created['id']]
    helper.modify_users(data)

    trainer_user_in_new_group = helper.get('/user/' + str(user_created['id']) + '?detail=True')
    assert trainer_user_in_new_group['groups'][0]['name'] == group_created['name']

    # check the user has now the role trainer
    user_role_ids = map(lambda e: e['id'], trainer_user_created['roles'])
    assert trainer_role['id'] in user_role_ids
    assert lingadmin_role['id'] in user_role_ids

    trainer_user_created = next(
        item for item in helper.get_users() if item['id'] == data['user_id'])

    # Now remove a role from the user
    data['roles'] = [lingadmin_role['id']]
    helper.modify_users(data)
    removed_role_user = helper.get('/user/' + str(trainer_user_created['id']) + '?detail=True')
    user_role_ids = [e['id'] for e in removed_role_user['roles']]
    assert trainer_role['id'] not in user_role_ids
    assert lingadmin_role['id'] in user_role_ids

    # Test: disable the user
    helper.post('user/disable', {'user_id': user_created['id']})
    # no way to to check the user is right disabled
    user_disabled = helper.get('user/' + str(user_created['id']) + '?all=True&detail=True')
    assert user_disabled['active'] is False

    # Test: enable the user
    helper.post('user/enable', {'user_id': user_created['id']})
    user_enabled = helper.get('user/' + str(user_created['id']) + '?all=True&detail=True')
    assert user_enabled['active'] is True

    # TEST: delete the user
    helper.post('user/delete', {'user_id': user_created['id']})
    user_ids = [[o['id'] for o in helper.get_users()]]
    assert user_created['id'] not in user_ids


"""
TEST: test_whoami
GOAL: add an user not admin, login with then check the user can get his role
"""


@pytest.mark.usefixtures("teardown_db")
def test_whoami(helper):
    user_email = 'lolo.fernandel@systran.fr'
    helper.set_user(user_email, '0123456789')
    user = helper.get("user/whoami")

    # check different fields
    assert user['email'] == user_email
    user_role_ids = map(lambda e: e['name'], user['roles'])
    assert user_role_ids
    assert 'user' in user_role_ids


"""
 TEST: test_group
 GOAL:
 - create an user with a role
 - give it a role
 - disable/enable/delete the use
"""


@pytest.mark.skip
@pytest.mark.usefixtures("teardown_db")
def test_group(helper):
    # prepare some test data

    helper.post("user/add",
                {'first_name': 'coco', 'last_name': 'belmondo', 'email': 'coco.belmondo@airbus.fr',
                 'password': 'Systran@123456', 'user_code': 'COC', 'entity_id': 3})
    user_created_1 = next(
        item for item in helper.get_users() if item['email'] == 'coco.belmondo@airbus.fr' and
        item['entity_id'] == 3)

    helper.post("user/add", {'first_name': 'coco2', 'last_name': 'belmondo2',
                             'email': 'coco.belmondo2@airbus.fr',
                             'password': 'Systran@123456',
                             'user_code': 'COL', 'entity_id': 3})
    user_created_2 = next(
        item for item in helper.get_users() if item['email'] == 'coco.belmondo2@airbus.fr' and
        item['entity_id'] == 3)

    # TEST : get groups list
    groups = helper.get('group/list?detail=True')
    assert len(groups) == 1

    # TEST: create a group, associate to Airbus Entity
    group_data = {'name': 'mytestgroup', 'entity_id': 3, 'roles': [4, 5],
                  'users': [user_created_1['id'],
                            user_created_2['id']]}
    helper.post('group/add', group_data)

    groups = helper.get('group/list?detail=True')

    group_created = next(
        item for item in groups if item['name'] == 'mytestgroup' and item['entity'] == 'airbus')

    assert len(group_created['users']) == 2
    assert group_created['users'][0]['id'] == user_created_1['id'] or group_created['users'][0][
        'id'] == user_created_2['id']
    assert group_created['users'][1]['id'] == user_created_1['id'] or group_created['users'][1][
        'id'] == user_created_2['id']
    assert len(group_created['roles']) == 2
    assert group_created['roles'][0]['id'] == 4 or group_created['roles'][0]['id'] == 5
    assert group_created['roles'][1]['id'] == 4 or group_created['roles'][1]['id'] == 5

    # TEST: get group by Id
    group_by_id = helper.get('group/' + str(group_created['id']) + '?detail=True')

    assert group_by_id['id'] == group_created['id']

    # Remove a role from the group
    group_data_modified = {'name': group_data['name'], 'group_id': group_created['id'],
                           'roles': [4],
                           'users': [user_created_1['id']]}

    helper.post('group/modify', group_data_modified)

    group_by_id = helper.get('group/' + str(group_created['id']) + '?detail=True')
    assert len(group_by_id['users']) == 1
    assert group_by_id['users'][0]['id'] == user_created_1['id']
    assert len(group_by_id['roles']) == 1
    assert group_by_id['roles'][0]['id'] == 4

    # TEST : delete group
    helper.post('group/delete', {'group_id': group_by_id['id']})
    group_ids = [[o['id'] for o in helper.get('group/list?detail=True')]]
    assert group_by_id['id'] not in group_ids


"""
 TEST: test_check_permission
 GOAL: check the user has the permissions on the entity
"""


@pytest.mark.usefixtures("teardown_db")
def test_check_permission(helper):
    permissions_admin_result = helper.post('user/permissions/check',
                                           {'permissions': [{'permission': 'admin'},
                                                            {'permission': 'admin_user'},
                                                            {'permission': 'delete_model'},
                                                            {'permission': 'train'},
                                                            {'permission': 'admin_entity',
                                                             'entity': 1}]})
    for permission in permissions_admin_result:
        assert permission['is_authorized'] is True

    # Login with an standard user and check its permission
    user_lolo = 'lolo.fernandel@systran.fr'
    helper.set_user(user_lolo, '0123456789')
    permissions_lolo = helper.post('user/permissions/check',
                                   {'permissions': [{'permission': 'admin'},
                                                    {'permission': 'admin_user'},
                                                    {'permission': 'delete_model'},
                                                    {'permission': 'user'},
                                                    {'permission': 'admin_entity',
                                                     'entity': 1}]})
    # check only permission 7 is authorized
    for permission in permissions_lolo:
        assert (permission['permission'] == 'user') == (permission['is_authorized'] is True)


"""
Test: test_error_transaction
Goal: this test must fail for now because the server cannot manage transaction.
"""


@pytest.mark.skip
@pytest.mark.usefixtures("teardown_db")
def test_error_transaction(helper):
    num_of_users_before = helper.count_user()
    # Cannot user twice with a user_code already existing
    helper.post("user/add", {'first_name': 'coco', 'last_name': 'belmondo',
                             'email': 'coco.belmondo@systran.fr', 'password': 'Systran@123456',
                             'user_code': 'LOL'}, 424)

    assert helper.count_user() == num_of_users_before

    # admin user cannot add user with other company
    airbus_entity_id = 3

    user_created_id = helper.post("user/add", {'first_name': 'coco', 'last_name': 'belmondo',
                                               'email': 'coco.belmondo@airbus.fr',
                                               'password': 'Systran@123456',
                                               'user_code': 'COC', 'entity_id': airbus_entity_id})

    assert user_created_id != 0


""" Test: test_scim_apis
 Goal:
 - Test api create group: create new entity + share role
 - Test api patch group: test add/remove role from entity
"""


@pytest.mark.usefixtures("teardown_db")
def test_scim_apis(helper):
    # test api create group
    systran_entity_id = 1
    spns_role = helper.add_role({'name': 'spns', 'entity_id': systran_entity_id, 'permissions': []})
    new_entity = helper.post("/scim/v2/Groups", {'schemas': ["urn:ietf:params:scim:schemas:core:2.0:Group"],
                                                 'displayName': 'New Entity', 'externalId': 'abc12345678',
                                                 'roles': [{"value": spns_role['id']}]})

    spns_shared_role = next(
        item for item in helper.get_roles() if item['name'] == "spns" and item['entity_id'] == systran_entity_id)
    shared_entities_codes = [e['entity_id'] for e in spns_shared_role["shared_entities"]]
    new_entity_id = new_entity['id']

    assert new_entity_id in shared_entities_codes

    # test api patch group
    # test operation add role
    translate_pro_role = helper.add_role({'name': 'translate_pro', 'entity_id': systran_entity_id, 'permissions': []})
    json_data = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [{
            "op": "add",
            "path": "roles",
            "value": [{"value": translate_pro_role['id']}]
        }]
    }
    helper.patch(f"/scim/v2/Groups/{new_entity_id}", json_data)

    translate_pro_shared_role = next(item for item in helper.get_roles() if
                                     item['name'] == "translate_pro" and item['entity_id'] == systran_entity_id)
    shared_entities_codes = [e['entity_id'] for e in translate_pro_shared_role["shared_entities"]]

    assert new_entity_id in shared_entities_codes

    # test operation remove role
    json_data = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [{
            "op": "remove",
            "path": "roles",
            "value": [{"value": translate_pro_role['id']}]
        }]
    }
    helper.patch(f"/scim/v2/Groups/{new_entity_id}", json_data)

    translate_pro_shared_role = next(item for item in helper.get_roles() if
                                     item['name'] == "translate_pro" and item['entity_id'] == systran_entity_id)
    shared_entities_codes = [e['entity_id'] for e in translate_pro_shared_role["shared_entities"]]

    assert new_entity_id not in shared_entities_codes
