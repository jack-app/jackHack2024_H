[戻る](../README.md)

本来であれば`GoogleCalenderAPIWrapper`は`APIWrapper`下に抽象化されるべきだがあまり階層が深くなっても仕方がないので、
`CalenderEventGenerator`,`CalenderEventRegister`と同じ階層に設置されている。

## main

エンドポイントを定義し、フロント-バックエンド間でやり取りするデータの構造を直接的に定めます。

## GoogleCalenderAPIWrapper

APIへのアクセスと取得したデータをdict型から各々適切な型に詰め替える作業に責任を持ちます。
継続開発者はこのWrapperがWrapperの責務から逸脱しないように注意してください。
[詳細](GoogleCalenderAPIWrapper/README.md)　。

## InterpackageObjects

各種APIWrapper,CalenderEventRegister,CalenderEventGenerator間でやり取りされるオブジェクト（型）を定義します。
[詳細](InterpackageObjects/README.md)

