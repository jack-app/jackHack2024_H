[戻る](../README.md)

# InterpackageObjects

各種APIWrapper,CalenderEventRegister,CalenderEventGenerator間でやり取りされるオブジェクト（型）を定義する。
極力シンプルなもののみ置く。

## dataTransgerObject

通称DTO。複雑な動作は行わず、データのアノテーションのみを目的とする。
初期化時にデータの妥当性も検証する。

## datetime_expansion - timespan

`timespan`は２つの`datetime`,`start`と`end`の閉区間として扱われる。つまり`start`はタイムスパンに含まれ、`end`もまた含まれる。
外部に提供するメソッドは`duration`と`concat`であり、比較的シンプルなクラス。

# 例外

ここで独自に定義される例外はないが、組み込み例外`ValueError`を送出しうる。
