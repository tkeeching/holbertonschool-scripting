#!/usr/bin/python3

"""
A function that queries the Reddit API and prints the title
of the first 10 hot posts listed for a given subreddit.
"""

import json
import urllib.error
import urllib.request


def top_ten(subreddit):
    """Prints the title of the first 10 hot posts listed for a given subreddit"""

    try:
        base_url = 'https://api.reddit.com'
        url_path = 'r/{}/hot?limit=9'.format(subreddit)
        headers = {'User-Agent': 'Holberton/1.0'}
        request = urllib.request.Request(
            '{}/{}'.format(base_url, url_path),
            headers=headers)
        response = urllib.request.urlopen(request)

        if response.status == 200:
            html = response.read()
            html_decoded = html.decode('utf8')
            kind = json.loads(html_decoded)['kind']
            data = json.loads(html_decoded)['data']

            if kind == 'Listing' and len(data['children']) > 0:
                for item in data['children']:
                    print(item['data']['title'])
            else:
                print('None')

    except urllib.error.HTTPError as http_error:
        return http_error
    except json.decoder.JSONDecodeError as json_error:
        return json_error

# Test
# if __name__ == '__main__':
#     top_ten = __import__('1-top_ten').top_ten
#     if len(sys.argv) < 2:
#         print("Please pass an argument for the subreddit to search.")
#     else:
#         top_ten(sys.argv[1])
