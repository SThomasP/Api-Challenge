from pymongo import MongoClient
from api_challenge.tests.api_framework import post, example_data_update, example_data_merged, example_data_basic, client


# test adding a document to the database using an api
def test_post_add(client):
    test_data = example_data_basic.copy()
    response = post(client, test_data)
    # check that it returned the correct status code
    assert 200 == response.status_code
    # check that the response is correct
    assert response.is_json
    assert {'message': 'data successfully added'} == response.get_json()
    with MongoClient() as mongo:
        db = mongo.challenge
        # find the data in the database
        data_object = db.integrations.find_one({'tenant': test_data['tenant'], 'integration_type': test_data['integration_type']})
        # check that there's something there
        assert data_object is not None
        data_object.pop('_id')
        # check that the data is correct.
        assert data_object == example_data_basic


# test updating existing data using the api
def test_post_update(client):
    test_data_one = example_data_basic.copy()
    test_data_two = example_data_update.copy()
    with MongoClient() as mongo:
        # write the initial data to the database
        db = mongo.challenge
        db.integrations.insert_one(test_data_one)
        # test the method
        response = post(client, test_data_two)
        # check the status code is correct
        assert 200 == response.status_code
        # check that it's a valid json and that it's correct
        assert response.is_json
        assert {'message': 'data successfully updated'} == response.get_json()
        # get the object from the database
        data_object = db.integrations.find_one({'tenant': test_data_one['tenant'], 'integration_type': test_data_one['integration_type']})
        # check that there is one
        assert data_object is not None
        # check that the ids are the same
        assert test_data_one['_id'] == data_object['_id']
        data_object.pop('_id')
        # check that the data is correct
        assert data_object == example_data_merged


# test that data can be added and then the same document gets updated
def test_post_add_then_update(client):
    test_data_one = example_data_basic.copy()
    test_data_two = example_data_update.copy()
    # check that they have the same tenant and integration type
    assert test_data_one['tenant'] == test_data_two['tenant']
    assert test_data_one['integration_type'] == test_data_two['integration_type']
    search_data = {'tenant': test_data_one['tenant'], 'integration_type': test_data_one['integration_type']}
    with MongoClient() as mongo:
        db = mongo.challenge

        # test the first response
        response_one = post(client, test_data_one)
        assert 200 == response_one.status_code
        assert response_one.is_json
        assert {'message': 'data successfully added'} == response_one.get_json()
        result_data_one = db.integrations.find_one(search_data)
        id_one = result_data_one.pop('_id')
        assert result_data_one == example_data_basic

        # test the second
        response_two = post(client, test_data_two)
        assert 200 == response_two.status_code
        assert response_two.is_json
        assert {'message': 'data successfully updated'} == response_two.get_json()
        result_data_two = db.integrations.find_one(search_data)
        id_two = result_data_two.pop("_id")
        assert result_data_two == example_data_merged

        # make sure that they have the same object_id
        assert id_one == id_two


# test adding two datasets with different integration types, they should create two different documents
def test_post_two_adds_same_tenant(client):
    test_data_one = example_data_basic.copy()
    test_data_two = example_data_update.copy()
    test_data_two['integration_type'] = 'pilot-scheduling-system'
    assert test_data_one['tenant'] == test_data_two['tenant']
    assert test_data_one['integration_type'] != test_data_two['integration_type']

    response_one = post(client, test_data_one)
    assert 200 == response_one.status_code
    assert response_one.is_json
    assert {'message': 'data successfully added'} == response_one.get_json()

    response_two = post(client, test_data_two)
    assert 200 == response_two.status_code
    assert response_two.is_json
    assert {'message': 'data successfully added'} == response_two.get_json()

    with MongoClient() as mongo:
        db = mongo.challenge
        assert db.integrations.count_documents({'tenant': test_data_one['tenant']}) == 2


# test adding two data sets with different tenants, they should create two different documents.
def test_post_two_adds_same_integration_type(client):
    test_data_one = example_data_basic.copy()
    test_data_two = example_data_update.copy()
    test_data_two['tenant'] = 'competitor'
    assert test_data_one['tenant'] != test_data_two['tenant']
    assert test_data_one['integration_type'] == test_data_two['integration_type']

    response_one = post(client, test_data_one)
    assert 200 == response_one.status_code
    assert response_one.is_json
    assert {'message': 'data successfully added'} == response_one.get_json()

    response_two = post(client, test_data_two)
    assert 200 == response_two.status_code
    assert response_two.is_json
    assert {'message': 'data successfully added'} == response_two.get_json()

    with MongoClient() as mongo:
        db = mongo.challenge
        # check that two documents were created
        assert db.integrations.count_documents({'integration_type': test_data_one['integration_type']}) == 2


# test that the request fails correctly when no tenant is included
def test_post_fail_no_tenant(client):
    test_data = example_data_basic.copy()
    test_data.pop('tenant')
    response = post(client, test_data)
    with MongoClient() as mongo:
        db = mongo.challenge
        assert db.integrations.find_one(test_data) is None
        assert 400 == response.status_code
        assert response.is_json
        assert {"error": 400, 'message': 'required variable(s) are missing'} == response.get_json()


# test that the request fails correctly when no integration type is included
def test_post_fail_no_integration_type(client):
    test_data = example_data_basic.copy()
    test_data.pop('integration_type')
    response = post(client, test_data)
    with MongoClient() as mongo:
        db = mongo.challenge
        assert db.integrations.find_one(test_data) is None
        assert 400 == response.status_code
        assert response.is_json
        assert {"error": 400, 'message': 'required variable(s) are missing'} == response.get_json()


# test that request fails correctly when the _id field is included
def test_post_fail_id_included(client):
    test_data = example_data_basic.copy()
    test_data['_id'] = "CompleteRubbish"
    response = post(client, test_data)
    with MongoClient() as mongo:
        db = mongo.challenge
        assert db.integrations.find_one(test_data) is None
        assert 400 == response.status_code
        assert response.is_json
        assert {"error": 400, 'message': 'illegal variable(s) were found'} == response.get_json()
