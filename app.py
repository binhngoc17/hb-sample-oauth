import requests
import json
import os
from flask import Flask, redirect, request as req

HB_HOST = 'https://core.honestbee.com'
AUTHORIZATION_URL = HB_HOST + '/oauth/authorize'
TOKEN_URL = HB_HOST + '/api/account/token'
ME_URL = HB_HOST + '/api/me'
app = Flask(__name__)
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
CALLBACK_URL = os.environ['CALLBACK_URL']


@app.route('/')
def index():
    url = '{url}?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&response_type=code'.format(
        url=AUTHORIZATION_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=CALLBACK_URL
    )
    return redirect(url)


@app.route('/token')
def token():
    code = req.args.get('code') or '<authorization code provided for localhost testing>'
    if not code:
        return 'You need to update the authorization code'

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": CALLBACK_URL,
    }
    token = requests.post(TOKEN_URL, data=data)
    with open('tokens.json', 'wb') as f:
        f.write(json.dumps(token.json()))

    return 'Tokens are saved in tokens.json'


@app.route('/me')
def me():
    access_token = json.load(open('tokens.json', 'r'))['access_token']

    user = requests.get(
        '{url}?access_token={access_token}'.format(
            access_token=access_token,
            url=ME_URL
        ))

    with open('me.json', 'wb') as f:
        f.write(json.dumps(user.json()))
    return 'User information is save at me.json'

if __name__ == '__main__':
    app.run(debug=True)
