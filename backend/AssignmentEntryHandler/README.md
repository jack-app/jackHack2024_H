本来であれば
`GoogleCalenderAPIWrapper`は
`APIWrapper`下に抽象化されるべきだが、
あまり階層が深くなっても仕方がないので、
`CalenderEventGenerator`,`CalenderEventRegister`と同じ階層に設置されている。

TODO: scheduleモジュールが複雑なので言及