from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails, ZillowNoResults,\
    ZillowError, ZillowFail


def pull_property_data(search_address, search_zip, zillow_key):
    zillow_wrapper = ZillowWrapper(zillow_key)
    search_response = zillow_wrapper.get_deep_search_results(search_address, search_zip)
    search_results = GetDeepSearchResults(search_response)
    # TODO: Store results in Mongo
    pass


def get_zillow_estimated_price(zillow_id, zillow_key):
    zillow_wrapper = ZillowWrapper(zillow_key)
    property_response = zillow_wrapper.get_updated_property_details(zillow_id)
    property_results = GetUpdatedPropertyDetails(property_response)
    # TODO: pyzillow doesn't get the price - write my own
    pass
