## 開発環境のセットアップ

https://fastapi.tiangolo.com/ja/tutorial/

`py -3.11 -m venv .venv`
を実行して、venvをインストールする。

venvをインストールしたら
`.venv\Scripts\activate.ps1`などを実行してvenvをアクティベートする

そのあと
`pip install -r backend\requirement.txt`を実行して依存関係をインストールする

## サーバーを立てる

`cd backend`の後
`uvicorn main:app --reload`

venvの有効化を忘れずに
