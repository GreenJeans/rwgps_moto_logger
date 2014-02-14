__author__ = 'tylermorita'

import json
import requests
from test_payloads import payload


session = requests.session()


def login(email, password):
    '''get and set a session token'''
    url = 'https://ridewithgps.com/users/current.json'
    params = {'android_version': 19,
             'device_manufacturer': 'motorola',
             'device_model': 'XT1060',
             'documentation_version': 1,
             'email': email,
             'app_version': '1.0.33',
             'password': password,
             'version': '2',
             'apikey': 'mzeanzgk'}
    resp = session.get(url, params=params)
    session.params = {'auth_token': resp.json()['user']['auth_token'],
                      'api_key': 'mzeanzgk'}
    return


def submit_trip(data):
    url = 'https://ridewithgps.com/trips'
    resp = session.post(url, data=data, headers={'content-type': 'application/json'})
    return resp


if __name__ == '__main__':
    login('tyler.morita@gmail.com', 'ch0k3r53773R')
    resp = submit_trip(json.dumps(payload))
    print resp.headers, resp.text