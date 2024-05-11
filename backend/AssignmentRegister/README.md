[戻る](../README.md)

# AssignmentRegister

エンドポイントを定義し、フロント-バックエンド間でやり取りするデータの構造を直接的に定める。

本来であれば`GoogleCalenderAPIWrapper`は`APIWrapper`下に抽象化されるべきだがあまり階層が深くなっても仕方がないので、
`CalenderEventGenerator`,`CalenderEventRegister`,...と同じく`AssignmentRegister`直下に配置されている。

## CalenderEventGenerator

AssignmentからCalenderEventを生成する。
[詳細](CalenderEventGenerator/README.md)

## CalenderEventRegister

CalenderEventを実際にカレンダーに登録する。
現状ではGoogleCalenderAPIWrapper/GoogleCalenderAPIClientのラッパー。
ただし、LINEBotへの通知機能などの拡張を考えると、この抽象化レイヤーは設置されるべきである。
[詳細](CalenderEventRegister/README.md)

## GoogleCalenderAPIWrapper

APIへのアクセスと取得したデータをdict型から各々対応する適切な型に詰め替える作業に責任を持ちます。
継続開発者はこのWrapperがWrapperの責務から逸脱しないように注意してください。
[詳細](GoogleCalenderAPIWrapper/README.md)　。

## InterpackageObjects

各種APIWrapper,CalenderEventRegister,CalenderEventGenerator間でやり取りされるオブジェクト（型）を定義します。
[詳細](InterpackageObject/README.md)

# 例外

想定された例外はない。（このパッケージですべてハンドリングされるべきである。）
ただし、ユーザー定義例外は必要であればHTTPExceptionを継承して定義されるため、この階層で行うべきこともない。
