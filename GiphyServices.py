import giphy_client
from giphy_client.rest import ApiException

def get_gifs(search_string):

    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC'
    query_str = search_string
    limit = 100
    offset = 0
    rating = 'g'
    lang = 'en'
    req_format = 'json'

    try:
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, query_str, limit=limit, offset=offset,
                                                    rating=rating, lang=lang, fmt=req_format)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

    list_of_gifs = api_response.data
    gif_links = []

    for gif_obj in list_of_gifs:
        gif_links.append(gif_obj.images.fixed_height_small.url)
    return gif_links