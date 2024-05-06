# 環境

## セットアップ

### windows

`py -3.11 -m venv .venv`
を実行して、venvをインストールする。そのあと
`pip install -r requirements-windows.txt`
を実行して依存関係をインストールする

### ubuntu

`python3.11 -m venv .venv`
を実行して、venvをインストールする。そのあと
`pip install -r requirements-ubuntu.txt`
を実行して依存関係をインストールする

## サーバーの起動

カレントディレクトリを`backend`(このREADME)があるファイルにして、
`uvicorn main:app --reload`

# 構成

## 概要

### DEPLOY_SETTING

デプロイする際に必要な設定や認証情報の設置場所であり、
これら情報を定数として提供する。

### AuthHandler

APIなどの利用に歳する認証フローを扱うプログラムがここに配置される。
今のところはGoogleCalenderAPIしか扱わないが、拡張性のために抽象化レイヤーとして置かれている。

### main *ENTRYPOINT

main: *エントリーポイント

依存関係を規定する。
サーバーを設定する。

## エラーハンドリング

依存先パッケージはパッケージ内の
`exceptions.py`
に定義される例外を返送する可能性がある。

エラーはどこでも送出される可能性があるが、エンドポイントを直接定義する関数において、フロント側へのレスポンスに変換される。