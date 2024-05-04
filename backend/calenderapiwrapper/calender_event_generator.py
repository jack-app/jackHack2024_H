"""
課題の一覧を受け取り、カレンダーに登録する
summary: 課題のタイトル = title
description: 課題の説明 = (courseName, courseId, dueDate)
start: 課題をやり始める時間 = 空いている時間に押し込む
end: 課題をやり終える = start + duration
"""
from calender_api_wrapper import CalenderAPIWrapper
from datetime import datetime, timedelta

class CalenderEventGenerator:
    """
    必要な関数
    0. それぞれの課題の情報を受け取って、締め切りの最大時間を取得する
    1. CalenderAPIWrapperを叩いて(0で取得した最大時間を関数の引数にする)
       空いている時間帯を取得する
    2. 空いている時間帯に課題を押し込むことを考える(区間スケジューリング)
    3. CalenderAPIWrapperを叩いて、課題をカレンダーに登録する
    """
    def __init__(self):
        self.calendar = CalenderAPIWrapper()

    def task_execute(self):
        """
        課題の一覧を受け取って、カレンダーに登録する
        """
        tasks = self.get_tasks()
        self.write_tasks(self.schedule_tasks(tasks))

    def get_max_due_date(self, tasks):
        """
        課題の一覧を受け取り、締め切りの最大時間を取得する
        """
        time_max = None
        time_max = max([task.dueDate for task in tasks])
        return time_max
    
    def get_free_time(self, time_max):
        """
        空いている時間帯を取得する
        """
        time_dict = {}#空いている->0, 予定がある->1以上
        if time_max == None:
            schedule = self.calendar.read_calendar()
        else:
            schedule = self.calendar.read_calendar(time_max)

        # start と end を datetime オブジェクトに変換
        starttime_dt = datetime(*schedule["start_time"])
        endtime_dt = datetime(*schedule["end_time"]) + timedelta(days=1)

        # start から end までのすべての日付を取得し、for ループで処理
        current_date = starttime_dt
        while current_date <= endtime_dt:
            time_dict[current_date.strftime("%Y-%m-%d %H:%M:%S")] = 0
            current_date += timedelta(minutes=1)  # 1 分進める

        for event in schedule["events"]:
            # start と end を datetime オブジェクトに変換
            start_dt = datetime(*event["start"])
            end_dt = datetime(*event["end"]) + timedelta(minutes=1)
            end_dt = min(end_dt, endtime_dt)
            time_dict[start_dt.strftime("%Y-%m-%d %H:%M:%S")] += 1
            time_dict[end_dt.strftime("%Y-%m-%d %H:%M:%S")] -= 1
        
        # start から end までのすべての日付を取得し、for ループで処理
        current_date = starttime_dt
        pre = 0
        while current_date <= endtime_dt:
            time_dict[current_date.strftime("%Y-%m-%d %H:%M:%S")] += pre
            pre = time_dict[current_date.strftime("%Y-%m-%d %H:%M:%S")]
            current_date += timedelta(minutes=1)  # 1 分進める
        return time_dict

    def schedule_tasks(self, tasks, free_time_list):
        """
        課題を空いている時間帯に押し込む
        """
        free_time_list = self.get_free_time(self.get_max_due_date(tasks))
        return free_time_list

    def write_tasks(self, tasks):
        """
        課題をカレンダーに登録する
        """
        for task in tasks:
            event = {
                'summary': task.title,
                'description': f"{task.courseName}, {task.courseId}, {task.dueDate}",
                'start': {
                    'dateTime': task.start,
                },
                'end': {
                    'dateTime': task.end,
                },
            }
            self.calendar.write_calendar(event)


if __name__ == "__main__":
    calendar = CalenderEventGenerator()
    res = calendar.get_free_time(None)
    print(res)