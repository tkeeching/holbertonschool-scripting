#!/usr/bin/python3

"""
A recursive function that queries the Reddit API and returns a list
containing the titles of all hot articles for a given subreddit.
"""

import json
import urllib.error
import urllib.request


def recurse(subreddit, hot_list=[], after=None):
    """
    Returns a list containing the titles of all hot articles for
    a given subreddit.
    If no results are found, return None
    """

    try:
        base_url = 'https://api.reddit.com'
        url_path = 'r/{}/hot'.format(subreddit)
        # headers = {'User-Agent': 'Holberton/1.0'}

        # Include 'after' parameter in URL if it exists
        if after:
            url_path += f'?after={after}'

        request = urllib.request.Request(
            '{}/{}'.format(base_url, url_path))
        response = urllib.request.urlopen(request)

        if response.status == 200:
            html = response.read()
            html_decoded = html.decode('utf8')
            kind = json.loads(html_decoded)['kind']
            data = json.loads(html_decoded)['data']
            children = data['children']

            if kind == 'Listing' and len(children) > 0:
                for child in children:
                    hot_list.append(child['data']['title'])

                if data['after']:
                    return recurse(subreddit, hot_list, data['after'])
                else:
                    return hot_list if hot_list else None
            else:
                return None

    except urllib.error.HTTPError as http_error:
        print(f"HTTP Error: {http_error.code}")
        return http_error
    except json.decoder.JSONDecodeError as json_error:
        print(f"JSON Decode Error: {json_error}")
        return json_error
