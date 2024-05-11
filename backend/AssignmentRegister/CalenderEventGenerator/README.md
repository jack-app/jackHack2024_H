[戻る](../README.md)

# GoogleCalenderEventGenerator

Assignmentを受け取ってCalenderEvent(s)を生成する。
一つのAssignmentに対して複数のCalenderEventを生成する可能性があることに注意するべし。
`generate_events`はAyncGeneratorである。
`main`が請け負っている処理は
- `Scheduler`を初期化すること
- `Scheduler`が返してきたtimespanをイベントに直すこと
のみで割とシンプル。

`sleepSchedule`がフロント（ユーザー）側から設定できないので改善の余地あり。

## CalenderEventScheduler

複雑な処理はコチラに隔離されていると考えていい。
追っている責務は課題を登録する時間区間(コード内ではchunkと呼ばれているtimespan型のオブジェクト)の算出である。
これは複数生成されうる。

[詳細](./CalenderEventScheduler/README.md)

# 例外

CalenderEventScheduler/bitmapFacotry/avoid_task_overlappingが
GoogleCalenderAPIWrapperに依存しているのでこの例外が送出される可能性がある。