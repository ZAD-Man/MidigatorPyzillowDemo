from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails, ZillowNoResults,\
    ZillowError, ZillowFail
from pymongo.mongo_client import MongoClient


def connect_to_mongo(mongo_connection_string=None):
    if mongo_connection_string is not None:
        client = MongoClient(mongo_connection_string)
    else:
        client = MongoClient()
    return client


def get_zestimate_from_response(zestimate_response):
    amount_location = 'response/zestimate/amount'
    amount = zestimate_response.findtext(amount_location)
    return amount


def pull_property_data(search_address, search_zip, zillow_key, mongo_connection_string=None):
    mongo_client = connect_to_mongo(mongo_connection_string)
    zillow_wrapper = ZillowWrapper(zillow_key)
    search_response = zillow_wrapper.get_deep_search_results(search_address, search_zip)
    search_results = GetDeepSearchResults(search_response)
    # TODO: Store results in Mongo
    pass


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
    zestimate_response = zillow_wrapper.get_data(url, params)
    zestimate = get_zestimate_from_response(zestimate_response)
    return zestimate
