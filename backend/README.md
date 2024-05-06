# 環境

## セットアップ

`py -3.11 -m venv .venv`
を実行して、venvをインストールする。
そのあと
`pip install -r requirement.txt`を実行して依存関係をインストールする

## サーバーの起動

`cd backend`の後
`uvicorn main:app --reload`

venvの有効化を忘れずに

# 構成

## main

main: *エントリーポイント
依存関係を規定する。