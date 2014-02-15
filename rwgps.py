__author__ = 'tylermorita'

import csv
import json
import requests
# from test_payloads import payload
import config

session = requests.session()


def login(email, password):
    '''get and set a session token'''
    url = 'http://beta.ridewithgps.com/users/current.json'
    params = {'android_version': 19,
              'device_manufacturer': 'motorola',
              'device_model': 'XT1060',
              'documentation_version': 1,
              'email': email,
              'app_version': '1.0.33',
              'password': password,
              'version': '2',
              'apikey': 'as90b8eu'}
    resp = session.get(url, params=params)
    session.params = {'auth_token': resp.json()['user']['auth_token'],
                      'api_key': 'as90b8eu'}
    print resp.json()['user']['auth_token']
    return


def submit_trip(data):
    url = 'http://beta.ridewithgps.com/trips'
    params = {'auth_token': config.auth_token,
              'api_key': 'as90b8eu'}
    resp = session.post(url, data=data, headers={'content-type': 'application/json'}, params=params)
    return resp


def make_payload(csv_file, name):
    csv_file = csv.DictReader(open(csv_file))
    data = []
    data_list = []
    for row in csv_file:
            data_list.append({"x": float(row['GPS Longitude']),
                          "y": float(row['GPS Latitude']),
                          "e": 10.0,
                          "t": int(str(int(row['time']) / 1000)),
                          "h": float(row['RPM']),
                          "s": float(row['GPS Speed']),
                          "c": float(row['Air Fuel Ratio (alt)']),
                          "p": float(row['Boost'])})

    payload = {'trip': {'bad_elevations': True,
                        'visibility': 0,
                        'name': name,
                        'is_gps': True}}
    payload['trip']['track_points'] = data_list
    return payload


if __name__ == '__main__':
    # login(config.email, config.password)
    payload = make_payload('1392401367846.csv', 'SO COOL')
    resp = submit_trip(json.dumps(payload))
    print resp.headers, resp.text