[戻る](../README.md)

# SignQueue

AuthHandler内でOAuthのフロー用に使用されることを意図したパッケージ。
発行されたStateを保持（あるいはstateを発行して保持）し、codeによるサインを受け付ける（サインを待つ。）

stateがcodeによりサインされると、そのstateをキーにして問い合わせたときcodeを返却する。
stateがサインされていない状態で問い合わせを受けると、しばらく(configで設定された時間)**非同期的**に待機し、それまでの間にサインされればcodeを返却し、
サインされなければ`TokenFechingTimeout`を送出する。

stateには有効期限が(configによって)設定でき、一定数以上のstateがキューに入ると期限切れのstateを廃棄する。

# 例外

`TokenFechingTimeout`を送出する可能性がある。ただしこれはHTTPExceptionsを継承しているため、特別ハンドリングをする必要はない。
