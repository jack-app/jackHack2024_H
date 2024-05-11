[戻る](../README.md)

# DEPLOY_SETTING

`client id`や`client secret`を設置する。
`.env`,`credentials.json`には重複する内容があるが、ともに必要であるのでどちらも配置すること。
`.env`に記載する内容については、環境変数として定めても良い。

`credentials.json`は
`https://console.cloud.google.com/apis/credentials`にアクセスし、OAuth 2.0クライアント IDに登録されているレコードから、`OAuthクライアントをダウンロード`>`jsonダウンロード`を選択してダウンロードする。`client_secret_xxx.json`という名前なので、リネームして配置すること。
事前に`OAuth同意画面`を構成しなければならないので注意。

`.env`の内容は`credentials.json`から対応するものを抜粋すれば良い。
ここに`.env`に記述するべき変数を示すと、

- CLIENT_ID
- CLIENT_SECRET
- REDIRECT_URI

である。

`REDIRECT_URI`はAuthHandlerが担当する認証フローで使われるものである。
`https://console.cloud.google.com/apis/credentials`にアクセスし、OAuth 2.0クライアント IDに登録されているレコードのクライアント名をクリックすると設定に飛び、
`認証リダイレクトURI`という項目があるので、ここにも`REDIRECT_URI`に設定するものと同じURIを登録しておくこと。さもなければ動かない。

`REDIRECT_URL`は`http://{domain_name}/oauth2callback`あるいは`https://{domain_name}/oauth2callback`のようになる。
ここでプロトコルも`認証リダイレクトURI`に登録したもと同じでなければならないことに注意。(`https`で登録していた場合、`http`では動かないし、逆もまた然りである。)

`CLIENT_ID`は`.apps.googleusercontent.com`で終わるもの。
`CLIENT_SECRET`については例示しないが、`client_id`,`client_secret`で`credentials.json`を検索すれば容易に見つかる。
