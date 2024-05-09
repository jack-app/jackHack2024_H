本来であれば`GoogleCalenderAPIWrapper`は`APIWrapper`下に抽象化されるべきだがあまり階層が深くなっても仕方がないので、
`CalenderEventGenerator`,`CalenderEventRegister`と同じ階層に設置されている。

## schedule

`timespan`, `FreeBusyBitMap`からなる。
`timespan`は２つの`datetime`の組であり、`FreeBusyBitMap`はこれに依存している。
`FreeBusyBitMap`は予定の有無をbit列上で表現したものである。
各bitは長さ`interval(timedelta)`の時間的な区間をエンコードしている。
