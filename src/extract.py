#!/usr/bin/env python3
#
# https://github.com/kaiterra/api/examples/restv1-urlkey.py
#
# This script demonstrates getting the latest data from a Laser Egg and Sensedge using the API.
#
# To use the script, do the following:
#  1. Use pip to install packages in requirements.txt (usually pip -r requirements.txt)
#  2. Change API_KEY to the key you created for your Kaiterra account on http://dashboard.kaiterra.cn/.
#  3. Run the script.  It will make the request, printing out information about the auth process
#     along the way.

from datetime import datetime, timezone
import sys
import requests
from dotenv import load_dotenv
import os
import io

load_dotenv()

API_BASE_URL = "https://api.kaiterra.cn/v1/"

API_KEY = os.getenv("API_KEY")

# Create a session object to reuse TCP connections to the server
session = requests.session()


def do_get(relative_url, *, params={}, headers={}):
    '''
    Executes an HTTP GET against the given resource.  The request is authorized using the given URL key.
    '''
    import json

    params['key'] = API_KEY

    url = API_BASE_URL.strip("/") + relative_url

    print("http: Fetching:   {}".format(url))
    print("http: Parameters: {}".format(params))
    print("http: Headers:  {}".format(headers))
    print()

    response = session.get(url, params=params, headers=headers)

    print("http: Status ({}), {} bytes returned:".format(
        response.status_code, len(response.content)))
    content_str = ''
    if len(response.content) > 0:
        content_str = response.content.decode('utf-8')
        print(content_str)
        print()

    response.raise_for_status()

    if len(content_str) > 0:
        return json.loads(content_str)

    return None


def get_devices(id: str):
    return do_get("/devices/" + id + "/top")


def summarize_devices(id: str):
    '''
    Prints top from /devices/
    '''
    devices = get_devices(id)

    for row in devices['data']:
        print("param: {}".format(row['param']))
    return


def check_available(name):
    import importlib
    try:
        _ = importlib.import_module(name, None)
    except ImportError:
        print("Missing module '{}'.  Please run this command and try again:".format(name))
        print("   pip -r requirements.txt")
        sys.exit(1)


def parse_rfc3339_utc(ts: str) -> datetime:
    '''
    Parses and returns the timestamp as a timezone-aware time in the UTC time zone.
    '''
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


if __name__ == "__main__":
    check_available("requests")
    from datetime import datetime, timezone

    summarize_devices("dd176486-7e5d-4c47-889b-6bfa0c588a65")
