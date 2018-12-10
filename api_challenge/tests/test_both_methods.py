from api_challenge.tests.api_framework import get, post, example_data_basic, example_data_update, example_data_merged, client


# test to see if the response gotten from a get request is the same as the one sent by a post
def test_add_get(client):
    test_data = example_data_basic.copy()
    response_one = post(client, test_data)
    assert 200 == response_one.status_code
    assert 'added' in response_one.get_json()['message']
    get_vars = {'tenant': test_data['tenant'], 'integration_type': test_data['integration_type']}

    response_two = get(client,get_vars)
    assert 200 == response_two.status_code
    assert response_two.is_json
    assert test_data == response_two.get_json()


# test to see whether the get request changes correctly after an update.
def test_add_update_get(client):
    initial_test_data = example_data_basic.copy()
    update_test_data = example_data_update.copy()
    response_one = post(client, initial_test_data)
    assert 200 == response_one.status_code
    assert 'added' in response_one.get_json()['message']
    get_vars = {'tenant': initial_test_data['tenant'], 'integration_type': initial_test_data['integration_type']}

    response_two = post(client, update_test_data)
    assert 200 == response_two.status_code
    assert 'updated' in response_two.get_json()['message']

    response_three = get(client,get_vars)
    assert 200 == response_three.status_code
    assert response_three.get_json() == example_data_merged


# test something a bit more complex, multiple pieces of data being added, retrived and updated.
def test_add_add_update_get_get(client):
    doc_one_data_initial = example_data_basic.copy()
    doc_one_data_update = example_data_update.copy()
    doc_two_data = example_data_basic.copy()
    doc_two_data['tenant'] = "big-corp"
    doc_two_data['integration_type'] = "something-else"
    doc_one_keys = {'tenant': doc_one_data_initial['tenant'], 'integration_type': doc_one_data_initial['integration_type']}
    doc_two_keys = {'tenant': doc_two_data['tenant'], 'integration_type': doc_two_data['integration_type']}

    request_one = post(client, doc_one_data_initial)
    assert 200 == request_one.status_code
    assert 'added' in request_one.get_json()['message']

    request_two = post(client, doc_one_data_update)
    assert 200 == request_two.status_code
    assert 'updated' in request_two.get_json()['message']

    request_three = post(client, doc_two_data)
    assert 200 == request_three.status_code
    assert 'added' in request_three.get_json()['message']

    request_four = get(client, doc_two_keys)
    assert 200 == request_four.status_code
    assert doc_two_data == request_four.get_json()

    request_five = get(client, doc_one_keys)
    assert 200 == request_five.status_code
    assert example_data_merged == request_five.get_json()

