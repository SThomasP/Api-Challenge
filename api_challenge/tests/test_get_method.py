from api_challenge.tests.api_framework import add_basic_example_data, get, client
from api_challenge.tests.api_framework import example_data_basic as example_data

# check that the method works correctly when the correct data is provided
def test_get_correct(client):
    add_basic_example_data()
    response = get(client, {'tenant': 'acme', 'integration_type': 'flight-information-system'})
    assert 200 == response.status_code
    assert response.is_json
    assert example_data == response.get_json()


# check to see that application responds correctly when no tenant is provided
def test_get_no_tenant(client):
    add_basic_example_data()
    response = get(client, {'integration_type': 'flight-information-system'})
    assert 400 == response.status_code
    assert response.is_json
    assert {'error': 400, "message": 'required variable(s) are missing'} == response.get_json()


# check to see that application responds correctly when no integration type is provided
def test_get_no_integration_id(client):
    add_basic_example_data()
    response = get(client, {'tenant': 'acme'})
    assert 400 == response.status_code
    assert response.is_json
    assert {'error': 400, "message": 'required variable(s) are missing'} == response.get_json()


# check to see that the application responds correctly when nothing is provided
def test_get_no_variables(client):
    add_basic_example_data()
    response = get(client, {})
    assert 400 == response.status_code
    assert response.is_json
    assert {'error': 400, "message": 'required variable(s) are missing'} == response.get_json()


# check to see that the application responds correctly when there is no data found for that combination of tenant and integration type.
def test_get_no_data(client):
    add_basic_example_data()
    response = get(client, {'tenant': 'no-one', 'integration_type': 'nothing'})
    assert 404 == response.status_code
    assert response.is_json
    assert {'error': 404, "message": 'data not found'} == response.get_json()
