import pytest
import api_challenge
from pymongo import MongoClient
from urllib.parse import urlencode

example_data_basic = {"tenant": "acme", "integration_type": "flight-information-system",
                      "configuration": {"username": "acme_user", "password": "acme12345",
                                        "wsdl_urls": {"session_url": "https://session.manager.svc",
                                                      "booking_url": "https://booking.manager.svc"}}}

example_data_update = {'tenant': 'acme', 'integration_type': 'flight-information-system',
                       'configuration': {"password": 'acme12345!', 'recovery_code': 'sdfajhqik',
                                         "wsdl_urls": {"session_url": "https://session.acme.svc",
                                                       "booking_url": "https://booking.acme.svc",
                                                       "recovery_url": "https://recovery.acme.svc"}}}

example_data_merged = {'tenant': 'acme', 'integration_type': 'flight-information-system',
                       'configuration': {'username': 'acme_user', "password": 'acme12345!', 'recovery_code': 'sdfajhqik',
                                         "wsdl_urls": {"session_url": "https://session.acme.svc",
                                                       "booking_url": "https://booking.acme.svc",
                                                       "recovery_url": "https://recovery.acme.svc"}}}


# pytest client
@pytest.fixture()
def client():
    api_challenge.app.config['TESTING'] = True
    client = api_challenge.app.test_client()

    with MongoClient() as mongo:
        db = mongo.challenge
        db.integrations.drop()
        db.create_collection("integrations")
        yield client

        db.integrations.drop()


# add test data to the database.
def add_basic_example_data():
    with MongoClient() as mongo:
        db = mongo.challenge
        db.integrations.insert_one(example_data_basic.copy())


# get function wrapper.
def get(client, args):
    args_str = urlencode(args)
    return client.get("/config?" + args_str)


# post function wrapper
def post(client, data):
    return client.post("/config", json=data.copy())
