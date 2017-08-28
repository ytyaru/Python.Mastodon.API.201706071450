import requests
import urllib.parse
import os.path
import json
import time
class Mastodon:
    def __init__(self, access_token, scheme='https', host='mstdn.jp'):
        self.scheme = scheme
        self.host = host
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer ' + access_token})

    def __build_url(self, path, query=None):
        if query:
            return urllib.parse.urlunsplit([self.scheme, self.host, path, query, ''])
        else:
            return urllib.parse.urlunsplit([self.scheme, self.host, path, '', ''])

    def __request(self, method, url, data=None, params=None):
        kwargs = {
            'data': data or {},
            'params': params or {}
        }
        r = self.session.request(method, url, **kwargs)
        r.raise_for_status()
        return r

    def home_timeline(self):
        url = self.__build_url('/api/v1/timelines/home')
        return self.__request('get', url)
    
    def toot(self, status):
        url = self.__build_url('/api/v1/statuses')
        return self.__request('post', url, data={'status': status})
    
    def all_home_timeline(self, since_id=None):
        path = '/api/v1/timelines/home'
        query = None
        if since_id: query = 'since_id={0}'.format(since_id)
        url = self.__build_url('/api/v1/timelines/home', query)
        print(url)
        r = self.__request('get', url)
        yield r.json()
        if 'next' not in r.links: return None
        print('has links URL:', r.links['next'])
        while ('next' in r.links):
            time.sleep(2)
            r = self.__request('get', r.links['next']['url'])
            yield r.json()


if __name__ == '__main__':
    access_token = 'アクセストークン'
    host = 'mstdn.jp'
    m = Mastodon(access_token, host=host)
    
    file_path = 'timeline.json'
    # 全件取得
    if not os.path.isfile(file_path):
        all_timeline = []
        with open(file_path, mode='w', encoding='utf-8') as f:
            for next_req_timeline in m.all_home_timeline():
                all_timeline.extend(next_req_timeline)
            f.write(json.dumps(all_timeline))
    # 保存済みの最新ID以降を取得
    else:
        all_timeline = None
        since_id = None
        with open(file_path, mode='r', encoding='utf-8') as f:
            all_timeline = json.loads(f.read())
            since_id = all_timeline[0]['id']
        with open(file_path, mode='a', encoding='utf-8') as f:
            append_line = []
            for next_req_timeline in m.all_home_timeline(since_id=since_id):
                append_line.extend(next_req_timeline)
            if 0 < len(append_line):
                f.write(json.dumps(all_timeline))
    
    # ファイル内にあるtoot(content)を表示する
    with open(file_path, mode='r', encoding='utf-8') as f:
        tm = json.loads(f.read())
        for line in tm:
#            print(line['content'])
            pass
        print('件数', len(tm))
