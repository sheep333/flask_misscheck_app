# [WIP]動作確認できていないので、手順確認して要修正

### git cloneでリポジトリのコピー

`git clone  xxxxxこのリポジトリxxxxxx`

### virtualenvをインストール

`pip3 install virtualenv`

### virtualenv(仮想環境の作成)

```
virtualenv venv

```

### virtualenvの有効化

`source venv/bin/activate`

(venv)という文字列がユーザー名の前に表示されていたら仮想環境が有効になっています。
この環境から抜けたい場合は`deactivate`で可能です。

### 必要なライブラリのインポート

```
pip install flask
pip install flask-sqlalchemy
pip install flask-wtf
```

### アプリの起動

```
python3 run.py
```

起動したら、下記のアドレスにアクセスして下さい。

http://127.0.0.1:5000

Flaskの日本語のリファレンスも一応あります。多少古いかも。

https://flask-docs-ja.readthedocs.io/en/latest/


### DBの確認ツール

便利なツールとしてSQLiteのDBをWebブラウザで表示するpythonのライブラリがあります。
https://github.com/coleifer/sqlite-web

`pip install sqlite-web`

`sqlite_web /path/to/database.db`

上記を実行するとポート8080で起動しました。

SQLiteのコマンドがMySQLと違ったりするので、新しいテーブル作成したりはGUIでやってもよいかも。
