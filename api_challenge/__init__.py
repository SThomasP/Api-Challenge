import flask
from pymongo import MongoClient


app = flask.Flask(__name__)


# merge a second dict into the first one, preserving as much of the hireachy as possible
def merge_dicts(merge_from, merge_into):
    # go through the keys to be merged in, seeing if they're in the original dict
    for key in merge_from.keys():
        if key in merge_into:
            # if the key is already in the dict get the type of data being stored at that key in both dicts
            merge_from_type = type(merge_from[key])
            merge_into_type = type(merge_into[key])
            # if they're both dicts, merge them recursively
            if merge_from_type == dict and merge_into_type == dict:
                merge_into[key] = merge_dicts(merge_from[key], merge_into[key])
            # if they're both lists, extend the original list with the new data
            elif merge_from_type == list and merge_into_type == list:
                merge_into[key].extend(merge_from[key])
            # any other combination, replace the old with the new
            else:
                merge_into[key] = merge_from[key]
        # if the key is not in the original dict, we can just add the new data
        else:
            merge_into[key] = merge_from[key]
    return merge_into


# generate an error status, based on a code and json.
def make_error(code, message):
    return flask.jsonify({'error': code, 'message': message}), code


# get function.
@app.route("/config", methods=['GET'])
def get_data():
    # check that both tenant and the integration_type have been specified
    if 'tenant' in flask.request.args and 'integration_type' in flask.request.args:
        tenant = flask.request.args['tenant']
        integration_type = flask.request.args['integration_type']
        with MongoClient() as mongo:
            db = mongo.challenge
            # get the data from the database
            db_object = db.integrations.find_one({'tenant': tenant, 'integration_type': integration_type})
            # make sure there is data there
            if db_object is not None:
                # get rid of the object id and then send it back
                db_object.pop('_id')
                return flask.jsonify(db_object), 200
            # if there is no data at that combination of tenant and integration type, return a 404
            else:
                return make_error(404, 'data not found')
    else:
        # if a variable is missing, return an error 400 (Bad request) with a message
        return make_error(400, "required variable(s) are missing")


# the post function
@app.route("/config", methods=['POST'])
def post_data():
    # get a dict of the data submitted
    data = flask.request.get_json()
    # make sure that the tenant and integration type are submitted, and also make sure that there is no _id field
    if 'tenant' in data and 'integration_type' in data and '_id' not in data:
        tenant = data['tenant']
        integration_type = data['integration_type']
        with MongoClient() as mongo:
            db = mongo.challenge
            # find the existing object if it exists
            db_object = db.integrations.find_one({'tenant': tenant, 'integration_type': integration_type})
            if db_object is None:
                # if not, then just insert the data and send a successful response.
                db.integrations.insert_one(data)
                return flask.jsonify({'message': "data successfully added"}), 200
            else:
                # if the data object already exists, merge the new data into the existing one.
                to_update = merge_dicts(data, db_object)
                # and then tell it to replace the existing data.
                db.integrations.replace_one({'tenant': tenant, 'integration_type': integration_type}, to_update)
                return flask.jsonify({'message': 'data successfully updated'}), 200
    elif '_id' in data:
        # if there is an _id specified, refuse the request (this prevents problems with id conflicts)
        return make_error(400, "illegal variable(s) were found")
    else:
        # or send an error if either the tenant or the integration type is missing.
        return make_error(400, 'required variable(s) are missing')
