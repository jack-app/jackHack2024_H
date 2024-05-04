## 開発環境のセットアップ

https://fastapi.tiangolo.com/ja/tutorial/

`py -3.11 -m venv .venv`
を実行して、venvをインストールする。

venvをインストールしたら
`.venv\Scripts\activate.ps1`などを実行してvenvをアクティベートする

そのあと
`pip install -r backend\requirement.txt`を実行して依存関係をインストールする

## サーバーを立てる

<<<<<<< HEAD
pip install -r backend\requirement.txt
=======
`cd backend`の後
`uvicorn main:app --reload`

venvの有効化を忘れずに
>>>>>>> d1e66a3a7b32f72bf4c17e32e78393d693126e6c
