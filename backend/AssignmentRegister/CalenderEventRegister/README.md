[戻る](../README.md)

# CalenderEventRegister

CalenderEventを実際にカレンダーに登録する。
現状ではGoogleCalenderAPIWrapper/GoogleCalenderAPIClientのラッパー。
ただし、LINEBotへの通知機能などの拡張を考えると、この抽象化レイヤーは設置されるべきである。

# 例外

GoogleCalenderAPIWrapperに依存しているのでこの例外が送出される可能性がある。