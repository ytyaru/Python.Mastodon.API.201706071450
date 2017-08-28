import requests
import requests_oauthlib
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import json

# OAuth2 クライアント登録
def register_app(client_name, host, redirect_uris='urn:ietf:wg:oauth:2.0:oob', scopes='read write follow'):
    data = {
        'client_name': client_name,
        'redirect_uris': redirect_uris,
        'scopes': scopes,
    }
    r = requests.post("https://{host}/api/v1/apps".format(host=host), data=data)
    r.raise_for_status()
    return r.json()

# アクセストークン取得
def fetch_token(client_id, client_secret, email, password, host, scope=('read', 'write', 'follow')):
    token_url = "https://{host}/oauth/token".format(host=host)
    client = LegacyApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, username=email, password=password,
                              client_id=client_id, client_secret=client_secret, scope=scope)
    return token


# API詳細: https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md
host = 'mstdn.jp' # 'pawoo.net'などマストドン鯖のドメイン名
client_name = 'test_client' # 任意
scopes = 'read write follow' # https://github.com/tootsuite/documentation/blob/master/Using-the-API/OAuth-details.md
d = register_app(client_name, host, scopes=scopes)
print(d)
with open('mastodon_client_' + host + '_' + client_name + '.json', mode='w', encoding='utf-8') as f:
    f.write(json.dumps(d))

email = '登録したメールアドレス'
password = '登録したパスワード'
token = fetch_token(d['client_id'], d['client_secret'], email, password, host, scopes.split())
print(token)
with open('mastodon_token_' + host + '_' + d['client_id'] + '.json', mode='w', encoding='utf-8') as f:
    f.write(json.dumps(token))

