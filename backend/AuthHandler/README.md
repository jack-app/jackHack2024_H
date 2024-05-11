[戻る](../README.md)

# AuthHandler

認証フロー（トークンの取得やリフレッシュ、廃止など）を扱うプログラムはここに配置される。

## SignQueue

AuthHandler内でOAuthのフロー用に使用されることを意図したパッケージ。
発行されたStateを保持（あるいはstateを発行して保持）し、非同期的にcodeによるサインを受け付ける（サインを待つ。）
[詳細](SignQueue/README.md)

## GoogleAPITokenHandler

SignQueueに依存している。
GoogleOAuthのラッパ。
[詳細](GoogleAPITokenHandler/README.md)
