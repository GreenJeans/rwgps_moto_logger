__author__ = 'tylermorita'

import csv
import json
import requests
# from test_payloads import payload
import config


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
    '''post the trip'''
    url = 'http://beta.ridewithgps.com/trips'
    resp = session.post(url, data=data)
    return resp


def make_payload(csv_file, name):
    '''turn a csv of engine data into a payload for upload'''
    csv_file = csv.DictReader(open(csv_file))
    track_points = []
    for row in csv_file:
        track_points.append({"x": float(row['GPS Longitude']),
                             "y": float(row['GPS Latitude']),
                             "e": 10.0,
                             "t": int(row['time']) / 1000,
                             "h": float(row['RPM']),
                             "s": round((float(row['GPS Speed']) * .447), 2),
                             "c": float(row['Air Fuel Ratio (alt)']),
                             "p": float(row['Boost'])})
    payload = {'trip': {'bad_elevations': True,
                        'visibility': 0,
                        'name': name,
                        'is_gps': True}}
    payload['trip']['track_points'] = track_points
    # print json.dumps(payload, indent=4, sort_keys=True)
    return payload


if __name__ == '__main__':
    session = requests.session()
    session.params = {'auth_token': config.auth_token,
                      'api_key': config.api_key}
    session.headers = {'content-type': 'application/json'}

    # login(config.email, config.password)
    payload = make_payload('1392425135096.csv', 'DriveHome')
    resp = submit_trip(json.dumps(payload))
    # print 'Request:\nHeaders:\n{}\n\nParams:\n{}\n\nBody:\n{}\n\n'.format(session.headers, session.params,
    #                                                                       json.dumps(payload, indent=4))
    print 'Response:\nHeaders:\n{}\n\nBody:\n{}'.format(resp.headers, resp.text)