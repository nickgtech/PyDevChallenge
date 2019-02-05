import giphy_client

from math import ceil
from Constants import API_KEY, SEARCH_LIMIT, RATING, LANG, JSON
from giphy_client.rest import ApiException
from Models import Keys, db
from Create import get_key

def get_gifs(search_string, offset):

    # get and instance of the api client and get the key
    client = giphy_client.DefaultApi()
    api_key = Keys.query.filter_by(name=API_KEY).first()

    try:
        # hit giphy's search endpoint
        response = client.gifs_search_get(api_key.key, search_string, limit=SEARCH_LIMIT, offset=int(offset),
                                                    rating=RATING, lang=LANG, fmt=JSON)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

    # Extract a list of fixed height urls from the response to display on the page.
    list_of_gifs = response.data
    gif_links = []

    for gif_obj in list_of_gifs:
        gif_links.append(gif_obj.images.fixed_height_small.url)
    return gif_links, response.pagination


# return the total pages needed for the search query
def get_pages(total):
    return ceil(total / 18)
