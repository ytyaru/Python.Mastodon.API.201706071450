# このソフトウェアについて

MastodonからHomeタイムラインを取得する。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
    * requests-oauthlib 0.8.0
        * requests 2.2.1
        * oauthlib 2.0.1
* pyenv 1.0.10
    * Python 3.6.1
        * requests-oauthlib 0.8.0
            * requests 2.17.3
            * oauthlib 2.0.2

## WebService

* [マストドン鯖一覧](http://k52.org/mastodon/)
    * [Mastodon (mstdn.jp)](https://mstdn.jp/)
* [マストドンWebAPI](https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md)

# 準備

## アカウント取得する

1. 任意のマストドン鯖をさがす
1. アカウントを取得する

マストドン鯖のドメイン名、メールアドレス、パスワードはあとで使うので控えておく。

## AccessTokenを取得する

### 編集

`ClientIdGetter.py`ファイルを開いて、以下の3箇所を編集する。

```python
host = 'mstdn.jp' # 'pawoo.net'などマストドン鯖のドメイン名
```
```python
email = '登録したメールアドレス'
password = '登録したパスワード'
```

### 実行

```sh
$ python3 ClientIdGetter.py
```

以下の2ファイルができる。

* `mastodon_client_....json`
* `mastodon_token_....json`

このファイル内にClientId、AccessTokenが入っている。これらはAPIを叩くための認証キーである。

## HomeTimelineをすべて取得してみる

### 編集

`Mastodon.py`ファイルを開く。

```python
if __name__ == '__main__':
    access_token = 'アクセストークン'
    host = 'mstdn.jp'
```

ホストとアクセストークンを設定する。

### 実行

```sh
$ python3 Mastodon.py
```

`timeline.json`ファイルにHomeTimelineがすべて保存される。

あとはjson形式を解析して自由に扱うだけ。

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

Library|License|Copyright
-------|-------|---------
[requests](http://requests-docs-ja.readthedocs.io/en/latest/)|[Apache-2.0](https://opensource.org/licenses/Apache-2.0)|[Copyright 2012 Kenneth Reitz](http://requests-docs-ja.readthedocs.io/en/latest/user/intro/#requests)
[requests-oauthlib](https://github.com/requests/requests-oauthlib)|[ISC](https://opensource.org/licenses/ISC)|[Copyright (c) 2014 Kenneth Reitz.](https://github.com/requests/requests-oauthlib/blob/master/LICENSE)
[oauthlib](https://github.com/idan/oauthlib)|[BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause)|[Copyright (c) 2011 Idan Gazit and contributors](https://github.com/idan/oauthlib/blob/master/LICENSE)

