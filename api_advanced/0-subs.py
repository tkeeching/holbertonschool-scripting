#!/usr/bin/python3

"""
A function that queries the Reddit API and returns the number
of subscribers (not active users, total subscribers) for a
given subreddit.
"""

import json
import urllib.error
import urllib.request


def number_of_subscribers(subreddit):
    """Returns the number of subscribers for a given subreddit"""

    try:
        base_url = 'https://api.reddit.com'
        url_path = 'r/{}/about'.format(subreddit)
        response = urllib.request.urlopen('{}/{}'.format(base_url, url_path))

        if response.status == 200:
            html = response.read()
            html_decoded = html.decode('utf8')
            kind = json.loads(html_decoded)['kind']
            data = json.loads(html_decoded)['data']

            if kind == 't5' and data['subscribers'] > 0:
                return data['subscribers']
            else:
                return 0

    except urllib.error.HTTPError as error:
        print('HTTP Error: {}'.format(error.reason))
