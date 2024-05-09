[戻る](../README.md)

# InterpackageObjects

各種APIWrapper,CalenderEventRegister,CalenderEventGenerator間でやり取りされるオブジェクト（型）を定義する。

## dataTransgerObject

通称DTO.複雑な動作は行わず、データのアノテーションのみを目的とする。
初期化時にデータの妥当性も検証する。

## schedule

`timespan`, `FreeBusyBitMap`からなる。
`timespan`は２つの`datetime`の組であり、`FreeBusyBitMap`はこれに依存している。
`FreeBusyBitMap`は予定の有無をbit列上で表現したものである。
各bitは長さ`interval(timedelta)`の時間的な区間をエンコードしている。
