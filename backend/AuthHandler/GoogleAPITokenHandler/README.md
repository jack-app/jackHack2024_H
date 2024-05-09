[戻る](../README.md)

# GoogleAPITokenHandler

必要な認証情報は`backend/CREDS`内に配置される。
SignQueueに依存している。
GoogleOAuthのラッパ。通信関連における非同期処理に対応している。
Redirectによってよりシンプルな実装が可能であると思われたが、Redirectを使用するとcookieが設定されない現象を確認したため、現在の少々複雑なプロトコルを用いている。

## トークン発行プロトコル

1. `APP/getAuthFlowState`にアクセスして`auth_url`を取得。このときstateがcookieとして保持される。
    - 内部的にstateがSignQueueに登録される
2. 取得した`auth_url`にアクセスして`google/oAuth`から`GoogleAPI AccessToken,RefreshToken`と交換するための`code`を取得しリダイレクトされる。
   ユーザーは取得した`code`と`state`をパラメータとして`APP/oauth2callback`（リダイレクト先）に渡す。
    - サーバーは渡されたcodeでstateをサインする。
3. stateをcookieとして`APP/getTokens`に渡し、`AccessToken,RefreshToken`をcookieとして得る。
    - stateをキューからpopし、codeを返却する。このcodeが内部的に`googleAPI AccessToken,RefreshToken`に変換される。

なお、SignQueueの非同期対応によって2.,3.はその順番が多少入れ替わっても良い。3.においてTimeoutを受け取った場合は、そのままリクエストを繰り返せば良い。

### 可能かと思われたがうまく行かなかったトークン発行プロトコル

参考として表題のプロトコルを書き示す。

1. `APP/getAuthURL`にアクセスして`auth_url`を取得する。
2. `auth_url`にアクセスして`code`を取得しリダイレクトされる。ユーザーは`APP/oauth2callback`(リダイレクト先)に`code`を渡して、これがそのまま内部的に`code`を`token`に変換し**cookieとして返却する。**

調査と試行の結果、リダイレクト先がcookieをセットすることができない(**cookieとして返却する**ことができない)現象が確認され、このプロトコルは機能不全となった。