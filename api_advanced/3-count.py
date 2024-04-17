#!/usr/bin/python3

"""
A recursive function that queries the Reddit API, parses the title of
all hot articles, and prints a sorted count of given keywords
(case-insensitive, delimiited by spaces)
"""

import json
import urllib.error
import urllib.request


def count_words(subreddit, word_list, after=None, counter={}):
    """
    Returns sorted count of given keywords
    """

    try:
        base_url = 'https://api.reddit.com'
        url_path = 'r/{}/hot'.format(subreddit)
        headers = {'User-Agent': 'Holberton/1.0'}

        # Include 'after' parameter in URL if it exists
        if after:
            url_path += f'?after={after}'

        request = urllib.request.Request(
            '{}/{}'.format(base_url, url_path),
            headers=headers)
        response = urllib.request.urlopen(request)

        if response.status == 200:
            html = response.read()
            html_decoded = html.decode('utf8')
            kind = json.loads(html_decoded)['kind']
            data = json.loads(html_decoded)['data']
            children = data['children']

            if kind == 'Listing' and len(children) > 0:
                for child in children:
                    # print('title -> {}'.format(child['data']['title']))
                    for keyword in word_list:
                        if keyword.lower() in child['data']['title'].lower():
                            # Increment keyword count or initialize to 1 if
                            # not present
                            counter[keyword.lower()] = counter.get(
                                keyword.lower(), 0) + 1
                    # print('title counter -> {}'.format(counter))

                if data['after']:
                    return count_words(
                        subreddit, word_list, data['after'], counter)
                else:
                    for key, value in sorted(counter.items()):
                        print('{}: {}'.format(key, value))
            else:
                return None

    except urllib.error.HTTPError as http_error:
        print(f"HTTP Error: {http_error.code}")
        return http_error
    except json.decoder.JSONDecodeError as json_error:
        print(f"JSON Decode Error: {json_error}")
        return json_error
