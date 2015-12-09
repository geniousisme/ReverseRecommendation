# -*- coding: utf-8 -*-
"""
Yelp Search API 2.0

This program demonstrates the capability of the Yelp API version 2.0
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/documentation for the API
documentation.

This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
import argparse
import json
import oauth2
import sys
import urllib
import urllib2

from pprint import pprint

from Auth import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET
from KeyWord.KeyWord import keywords_search

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'New York, NY'
SEARCH_LIMIT = 10
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

reviews ="""
I am a regular customer and today I bought their special, lamb on spine and ribs, for $9.75.  I have enjoyed this dish before at Xi'an, but today there was virtually no meat on the bones.  When I brought it back, they refused to exchange it, saying I had already eaten it.  Well, it's true I had bitten into the assortment of bones to try and find some meat.  I then had an argument with the owner on the phone, who insisted that he could not exchange the special due to his store policy, which is not to take back any dish that has been eaten.
It's not as if I ate a dish of noodles and tried to return an empty tray.  I brought back the bones and gristle, which was most of the dish.
Why would you want to treat a regular customer, or any customer for that matter, this way?  I had never before returned a dish, and was actually on friendly terms with the young owner.   Maybe he should have given me the benefit of the doubt, since he was not even there.  Instead, he has lost a customer and gotten this bad review.
"""

def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    i = 0
    # for i in xrange(SEARCH_LIMIT):
    business_id = businesses[i]['id']

    print u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id)
    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    return response

def query_result():
    try:
        # infile = open("KeyWord/doc/test_review.txt", 'r')
        # reviews = infile.read()
        keywords = keywords_search(reviews)
        return query_api(keywords, DEFAULT_LOCATION)
    except urllib2.HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0}. Abort program.'.format(error.code))

if __name__ == '__main__':
    pprint(query_result(), indent=2)