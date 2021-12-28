import requests
import json
import os

from dotenv import load_dotenv

STATE = 'channels.json'

load_dotenv()  # take environment variables from .env.

DOMAIN = os.getenv('SLACK_DOMAIN')

cookies = {
    'd': os.getenv('SLACK_COOKIES_D'),
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'https://app.slack.com',
    'DNT': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers',
    'Authorization': 'Bearer ' + os.getenv('SLACK_TOKEN')
}

def api_call_post(endpoint, data):
    return requests.post('https://' + DOMAIN + '/api/' + endpoint,
        headers=headers,
        cookies=cookies,
        json=data
    )

def api_call(endpoint, data):
    return requests.get('https://' + DOMAIN + '/api/' + endpoint,
        headers=headers,
        cookies=cookies,
        params=data
    )

def refresh_channels():
    with open(STATE, 'w') as file_object:  #open the file in write mode
        channels = []
        cursor = None
        while True:
            print('Getting channels')
            res = api_call('conversations.list', {'cursor': cursor}).json()
            channels += res['channels']
            print(res['response_metadata'])
            cursor = res['response_metadata']['next_cursor']
            print(cursor)
            if not cursor:
                break
        print('Saving {} channels'.format(len(channels)))
        json.dump(channels, file_object, indent=4)

def apply_changes():
    with open(STATE, 'r') as file_object:  #open the file in write mode
        channels = json.load(file_object)

    for channel in channels:
        print(channel['name'], 'rename' in channel)
        if 'rename' in channel:
            api_call_post('conversations.rename', {
                "channel": channel['id'],
                "name": channel['rename'],
            })
            channel['name'] = channel['rename']
            del channel['rename']

    with open(STATE, 'w') as file_object:  #open the file in write mode
        print('Saving {} channels'.format(len(channels)))
        json.dump(channels, file_object, indent=4)

refresh_channels()
apply_changes()
