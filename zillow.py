import sys
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, ZillowError
from pymongo.mongo_client import MongoClient


def connect_to_mongo(mongo_connection_string=None):
    """
    Connects to mongo
    :param mongo_connection_string: String with mongo credentials URI, e.g. mongodb://uname:pass@host:port
                                    See https://docs.mongodb.com/v3.0/reference/connection-string/
                                    If None, connects to localhost:27017
    :return: Connected mongo client
    """
    if mongo_connection_string is not None:
        client = MongoClient(mongo_connection_string)
    else:
        client = MongoClient()
    return client


def get_zestimate_from_response(zestimate_response):
    """
    Takes the response from a GetZestimate call and returns the Zestimate amount
    :param zestimate_response: Result of a Zillow API GetZestimate call
    :return: Zestimate amount from the response (str)
    """
    amount_location = 'response/zestimate/amount'
    amount = zestimate_response.findtext(amount_location)
    return amount


def pull_property_data(search_address, search_zip, zillow_key, mongo_connection_string=None, update=False):
    """
    Gets property data for given address/zip and writes it to given mongo database
    Will write to zillow.property_data in mongo
    :param search_address: Address to search for
    :param search_zip: ZIP code to search for
    :param zillow_key: Zillow API key
    :param mongo_connection_string: String with mongo credentials URI, e.g. mongodb://uname:pass@host:port
                                    See https://docs.mongodb.com/v3.0/reference/connection-string/
    :param update: If True, and a document with found zillow_id already exists, updates that document, otherwise ignores
    :return: Mongo info if inserted/updated, else None
    """
    mongo_client = connect_to_mongo(mongo_connection_string)
    zillow_wrapper = ZillowWrapper(zillow_key)
    try:
        search_response = zillow_wrapper.get_deep_search_results(search_address, search_zip)
        search_results = GetDeepSearchResults(search_response)
    except ZillowError as ze:
        # Write a better error message
        error_string = "Zillow error %s: %s\n" % (ze.message['code'], ze.message['text'])
        sys.stderr.write(error_string)
        raise
    result_data = vars(search_results)

    # We don't want the xml data in there
    try:
        del result_data['data']
    except KeyError:
        pass

    zillow_db = mongo_client.zillow
    query = {
        'zillow_id': result_data['zillow_id']
    }

    mongo_info = None
    if update:
        update = {
            '$set': result_data,
        }
        options = {
            'upsert': True,
        }
        mongo_info = zillow_db.property_data.update(query, update, options)
    else:
        if zillow_db.property_data.find(query).count() == 0:
            mongo_info = zillow_db.property_data.insert(result_data)

    return mongo_info


def get_zestimate(zillow_id, zillow_key):
    """
    Uses Zillow's GetZestimate service to look up the Zestimate for a given property ID
    :param zillow_id: ID of the property to look up
    :param zillow_key: Zillow API key
    :return: The property's Zestimate (str)
    """
    url = 'http://www.zillow.com/webservice/GetZestimate.htm'
    params = {
        'zpid': zillow_id,
        'zws-id': zillow_key,
    }

    zillow_wrapper = ZillowWrapper(zillow_key)
    try:
        zestimate_response = zillow_wrapper.get_data(url, params)
    except ZillowError as ze:
        # Write a better error message
        error_string = "Zillow error %s: %s\n" % (ze.message['code'], ze.message['text'])
        sys.stderr.write(error_string)
        raise
    zestimate = get_zestimate_from_response(zestimate_response)
    return zestimate
